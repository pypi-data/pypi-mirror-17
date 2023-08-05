#--------------------------------------------------------------------
# Xeno: The Python dependency injector from outer space.
#
# Author: Lain Supe (lainproliant)
# Date: Sunday, August 28th 2016
#
# Released under a 3-clause BSD license, see LICENSE for more info.
#--------------------------------------------------------------------
import inspect

#--------------------------------------------------------------------
class InjectionError(Exception):
    pass

#--------------------------------------------------------------------
class MethodInjectionError(InjectionError):
    def __init__(self, method, name, reason = None):
        super().__init__('Failed to inject "%s" into method "%s".' % (
            name,
            method.__qualname__) + reason or "")
        self.method = method
        self.name = name

#--------------------------------------------------------------------
class ClassInjectionError(InjectionError):
    def __init__(self, clazz, name, reason = None):
        super().__init__('Failed to inject "%s" into constructor for class "%s".' % (
            name,
            clazz.__qualname__) + reason or "")
        self.clazz = clazz
        self.name = name

#--------------------------------------------------------------------
def singleton(f):
    """
    Method annotation indicating a named singleton resource.

    The function will only ever be invoked on an instance of the
    module once, and the return value will be provided to all
    injected objects that require it.
    """

    f._xeno_singleton = True
    f._xeno_provider = True
    return f

#--------------------------------------------------------------------
def provide(f):
    """
    Method annotation indicating a named resource.

    The function will be added to the Injector's resource map and
    called each time an injected instance is created that requires
    the resource.
    """

    f._xeno_provider = True
    return f

#--------------------------------------------------------------------
def inject(f):
    """
    Method annotation indicating an injection point in an object.

    Instance methods marked with @inject are called after an object
    is created via Injector.create() or if an instance is passed
    to Injector.inject().

    All of the parameters of a method marked with @inject must refer
    to named resources in the Injector, or must provide default values
    which can be overridden by resources in the injector.
    """
    f._xeno_injection_point = True
    return f

#--------------------------------------------------------------------
class Injector:
    """
    An object responsible for collecting resources from modules and
    injecting them into newly created instances.

    An Injector is instantianted with any number of modules, which
    provide resources via methods annotated with @provide.  These
    methods are allowed to depend on other resources, potentially
    from myriad other modules, in order to generate their
    dependencies.

    Evaulation and injection of dependencies is lazy, meaning that
    the dependency graph is not evaluated until a resource is
    requested.
    """
    def __init__(self, *modules):
        """
        Create an Injector object.

        *modules: A list of modules to include in the injector.
                  More modules can be added later by calling
                  Injector.add_module().
        """
        self.resources = {'injector': lambda: self}
        self.singletons = {}
        for module in modules:
            self.add_module(module)
    
    def add_module(self, module):
        """
        Add a module to the injector.  The module is scanned for @provider
        annotated methods, and these methods are added as resources to
        the injector.
        """
        self._scan_module_for_providers(module)

    def create(self, clazz, lazy = False):
        """
        Create an instance of the specified class.  The class' constructor
        must follow the rules for @inject methods, such that all of its
        parameters refer to injectable resources or are optional.

        If the object needs to be constructed with objects not from the
        Injector, do not use this method.  Instead, instantiate the object
        with these parameters in the constructor, then mark one or more
        methods with @inject and pass the instance to Injector.inject().
        """
        ctor_params, default_set = self._get_injection_params(clazz.__init__, unbound_ctor = True)

        try:
            kwargs = self._get_injection_kwargs(ctor_params, default_set)
        except MethodInjectionError as e:
            raise ClassInjectionError(clazz, e.name)
        
        instance = clazz(**kwargs)
        self._inject_instance(instance, lazy)
        return instance

    def inject(self, obj, lazy = False):
        """
        Inject a method or object instance with resources from this Injector.
        
        obj: A method or object instance.  If this is a method, all named
             parameters are injected from the Injector.  If this is an instance,
             its methods are scanned for injection points and these methods
             are all invoked with resources from the Injector.
        lazy (default False): Whether resource mappings should be lazy.  If True,
             instead of mapping resources immediately, the mapping is performed
             when the method is invoked.  This allows additional modules to be
             added later that change the resources used by the method or object.
        """
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            return self._inject_method(obj, lazy)
        else:
            return self._inject_instance(obj, lazy)
    
    def require(self, name, method = None):
        """
        Require a named resource from this Injector.  If it can't be provided,
        an InjectionError is raised.

        Optionally, a method can be specified.  This indicates the method that
        requires the resource for injection, and causes this method to throw
        MethodInjectionError instead of InjectionError if hte resource was
        not provided.
        """
        if not name in self.resources:
            if method is not None:
                raise MethodInjectionError(method, name, 'Resource was not provided.')
            else:
                raise InjectionError('The required resource "%s" was not provided.' % name)
        else:
            return self.resources[name]()

    def has(self, name):
        """
        Determine if this Injector has been provided with the named resource.
        """
        return name in self.resources

    def _bind_resource(self, name, bound_method):
        injected_method = self.inject(bound_method)
        if hasattr(bound_method, '_xeno_singleton'):
            def wrapper():
                if not name in self.singletons:
                    singleton = injected_method()
                    self.singletons[name] = singleton
                    return singleton
                else:
                    return self.singletons[name]
            self.resources[name] = wrapper
        else:
            self.resources[name] = injected_method
    
    def _get_injection_kwargs(self, params, default_set):
        kwargs = {}
        for param in params:
            if param in default_set and not self.has(param):
                continue
            kwargs[param] = self.require(param)
        return kwargs

    def _get_injection_params(self, method, unbound_ctor = False):
        sig = inspect.signature(method)
        injection_param_names = []
        default_param_set = set()
        params = list(sig.parameters.values())

        if not inspect.ismethod(method) and unbound_ctor:
            # Don't try to inject the 'self' parameter of an
            # unbound constructor.
            params = params[1:]

        for param in params:
            if param.kind in [inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY]:
                if param.default != param.empty:
                    default_param_set.add(param.name)
                injection_param_names.append(param.name)
            else:
                raise InjectionError('xeno.Injector only supports injection of POSITIONAL_OR_KEYWORD and KEYWORD_ONLY arguments, %s arguments (%s) are not supported.' % (
                    param.kind, param.name))
        return injection_param_names, default_param_set

    def _inject_instance(self, instance, lazy):
        return self._scan_instance_for_injection_points(instance, lazy)
    
    def _inject_method(self, method, lazy):
        params, default_set = self._get_injection_params(method)

        if lazy:
            def wrapper():
                kwargs = self._get_injection_kwargs(params, default_set)
                return method(*kwargs)
            return wrapper
        else:
            kwargs = self._get_injection_kwargs(params, default_set)
            def wrapper():
                return method(**kwargs)
            return wrapper

    def _scan_instance_for_injection_points(self, instance, lazy):
        members = inspect.getmembers(instance,
                                     predicate=inspect.ismethod)
        for name, bound_method in members:
            if hasattr(bound_method, '_xeno_injection_point'):
                self.inject(bound_method, lazy)()
        return instance

    def _scan_module_for_providers(self, module):
        members = inspect.getmembers(module,
                                     predicate=inspect.ismethod)
        for name, bound_method in members:
            if hasattr(bound_method, '_xeno_provider'):
                self._bind_resource(name, bound_method)

