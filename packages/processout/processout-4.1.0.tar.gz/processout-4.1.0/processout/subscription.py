try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

from .processout import ProcessOut
from .networking.response import Response

try:
    from .activity import Activity
except ImportError:
    import sys
    Activity = sys.modules[__package__ + '.activity']
try:
    from .authorizationrequest import AuthorizationRequest
except ImportError:
    import sys
    AuthorizationRequest = sys.modules[__package__ + '.authorizationrequest']
try:
    from .customer import Customer
except ImportError:
    import sys
    Customer = sys.modules[__package__ + '.customer']
try:
    from .token import Token
except ImportError:
    import sys
    Token = sys.modules[__package__ + '.token']
try:
    from .event import Event
except ImportError:
    import sys
    Event = sys.modules[__package__ + '.event']
try:
    from .gateway import Gateway
except ImportError:
    import sys
    Gateway = sys.modules[__package__ + '.gateway']
try:
    from .gatewayconfiguration import GatewayConfiguration
except ImportError:
    import sys
    GatewayConfiguration = sys.modules[__package__ + '.gatewayconfiguration']
try:
    from .invoice import Invoice
except ImportError:
    import sys
    Invoice = sys.modules[__package__ + '.invoice']
try:
    from .customeraction import CustomerAction
except ImportError:
    import sys
    CustomerAction = sys.modules[__package__ + '.customeraction']
try:
    from .project import Project
except ImportError:
    import sys
    Project = sys.modules[__package__ + '.project']
try:
    from .refund import Refund
except ImportError:
    import sys
    Refund = sys.modules[__package__ + '.refund']
try:
    from .tailoredinvoice import TailoredInvoice
except ImportError:
    import sys
    TailoredInvoice = sys.modules[__package__ + '.tailoredinvoice']
try:
    from .transaction import Transaction
except ImportError:
    import sys
    Transaction = sys.modules[__package__ + '.transaction']
try:
    from .webhook import Webhook
except ImportError:
    import sys
    Webhook = sys.modules[__package__ + '.webhook']

from .networking.requestprocessoutprivate import RequestProcessoutPrivate


class Subscription:

    def __init__(self, instance = None):
        if instance == None:
            instance = ProcessOut.getDefault()

        self._instance = instance

        self._id = ""
        self._project = None
        self._customer = None
        self._token = None
        self._url = ""
        self._name = ""
        self._amount = ""
        self._currency = ""
        self._metadata = {}
        self._returnUrl = ""
        self._cancelUrl = ""
        self._interval = ""
        self._trialPeriod = "0d"
        self._activated = False
        self._ended = False
        self._endedReason = ""
        self._sandbox = False
        self._createdAt = ""
        
    @property
    def id(self):
        """Get id"""
        return self._id

    @id.setter
    def id(self, val):
        """Set id
        Keyword argument:
        val -- New id value"""
        self._id = val
        return self
    
    @property
    def project(self):
        """Get project"""
        return self._project

    @project.setter
    def project(self, val):
        """Set project
        Keyword argument:
        val -- New project value"""
        if isinstance(val, Project):
            self._project = val
        else:
            obj = Project(self._instance)
            obj.fillWithData(val)
            self._project = obj
        return self
    
    @property
    def customer(self):
        """Get customer"""
        return self._customer

    @customer.setter
    def customer(self, val):
        """Set customer
        Keyword argument:
        val -- New customer value"""
        if isinstance(val, Customer):
            self._customer = val
        else:
            obj = Customer(self._instance)
            obj.fillWithData(val)
            self._customer = obj
        return self
    
    @property
    def token(self):
        """Get token"""
        return self._token

    @token.setter
    def token(self, val):
        """Set token
        Keyword argument:
        val -- New token value"""
        if isinstance(val, Token):
            self._token = val
        else:
            obj = Token(self._instance)
            obj.fillWithData(val)
            self._token = obj
        return self
    
    @property
    def url(self):
        """Get url"""
        return self._url

    @url.setter
    def url(self, val):
        """Set url
        Keyword argument:
        val -- New url value"""
        self._url = val
        return self
    
    @property
    def name(self):
        """Get name"""
        return self._name

    @name.setter
    def name(self, val):
        """Set name
        Keyword argument:
        val -- New name value"""
        self._name = val
        return self
    
    @property
    def amount(self):
        """Get amount"""
        return self._amount

    @amount.setter
    def amount(self, val):
        """Set amount
        Keyword argument:
        val -- New amount value"""
        self._amount = val
        return self
    
    @property
    def currency(self):
        """Get currency"""
        return self._currency

    @currency.setter
    def currency(self, val):
        """Set currency
        Keyword argument:
        val -- New currency value"""
        self._currency = val
        return self
    
    @property
    def metadata(self):
        """Get metadata"""
        return self._metadata

    @metadata.setter
    def metadata(self, val):
        """Set metadata
        Keyword argument:
        val -- New metadata value"""
        self._metadata = val
        return self
    
    @property
    def returnUrl(self):
        """Get returnUrl"""
        return self._returnUrl

    @returnUrl.setter
    def returnUrl(self, val):
        """Set returnUrl
        Keyword argument:
        val -- New returnUrl value"""
        self._returnUrl = val
        return self
    
    @property
    def cancelUrl(self):
        """Get cancelUrl"""
        return self._cancelUrl

    @cancelUrl.setter
    def cancelUrl(self, val):
        """Set cancelUrl
        Keyword argument:
        val -- New cancelUrl value"""
        self._cancelUrl = val
        return self
    
    @property
    def interval(self):
        """Get interval"""
        return self._interval

    @interval.setter
    def interval(self, val):
        """Set interval
        Keyword argument:
        val -- New interval value"""
        self._interval = val
        return self
    
    @property
    def trialPeriod(self):
        """Get trialPeriod"""
        return self._trialPeriod

    @trialPeriod.setter
    def trialPeriod(self, val):
        """Set trialPeriod
        Keyword argument:
        val -- New trialPeriod value"""
        self._trialPeriod = val
        return self
    
    @property
    def activated(self):
        """Get activated"""
        return self._activated

    @activated.setter
    def activated(self, val):
        """Set activated
        Keyword argument:
        val -- New activated value"""
        self._activated = val
        return self
    
    @property
    def ended(self):
        """Get ended"""
        return self._ended

    @ended.setter
    def ended(self, val):
        """Set ended
        Keyword argument:
        val -- New ended value"""
        self._ended = val
        return self
    
    @property
    def endedReason(self):
        """Get endedReason"""
        return self._endedReason

    @endedReason.setter
    def endedReason(self, val):
        """Set endedReason
        Keyword argument:
        val -- New endedReason value"""
        self._endedReason = val
        return self
    
    @property
    def sandbox(self):
        """Get sandbox"""
        return self._sandbox

    @sandbox.setter
    def sandbox(self, val):
        """Set sandbox
        Keyword argument:
        val -- New sandbox value"""
        self._sandbox = val
        return self
    
    @property
    def createdAt(self):
        """Get createdAt"""
        return self._createdAt

    @createdAt.setter
    def createdAt(self, val):
        """Set createdAt
        Keyword argument:
        val -- New createdAt value"""
        self._createdAt = val
        return self
    

    def fillWithData(self, data):
        """Fill the current object with the new values pulled from data
        Keyword argument:
        data -- The data from which to pull the new values"""
        if "id" in data.keys():
            self.id = data["id"]
        if "project" in data.keys():
            self.project = data["project"]
        if "customer" in data.keys():
            self.customer = data["customer"]
        if "token" in data.keys():
            self.token = data["token"]
        if "url" in data.keys():
            self.url = data["url"]
        if "name" in data.keys():
            self.name = data["name"]
        if "amount" in data.keys():
            self.amount = data["amount"]
        if "currency" in data.keys():
            self.currency = data["currency"]
        if "metadata" in data.keys():
            self.metadata = data["metadata"]
        if "return_url" in data.keys():
            self.returnUrl = data["return_url"]
        if "cancel_url" in data.keys():
            self.cancelUrl = data["cancel_url"]
        if "interval" in data.keys():
            self.interval = data["interval"]
        if "trial_period" in data.keys():
            self.trialPeriod = data["trial_period"]
        if "activated" in data.keys():
            self.activated = data["activated"]
        if "ended" in data.keys():
            self.ended = data["ended"]
        if "ended_reason" in data.keys():
            self.endedReason = data["ended_reason"]
        if "sandbox" in data.keys():
            self.sandbox = data["sandbox"]
        if "created_at" in data.keys():
            self.createdAt = data["created_at"]
        
        return self

    def customer(self, options = None):
        """Get the customer owning the subscription.
        Keyword argument:
		
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/subscriptions/" + quote_plus(self.id) + "/customers"
        data    = {

        }

        response = Response(request.get(path, data, options))
        body = response.body
        body = body["customer"]
        customer = Customer(instance)
        return customer.fillWithData(body)
        
    def customerAction(self, gatewayConfigurationId, options = None):
        """Get the customer action needed to be continue the subscription authorization flow on the given gateway.
        Keyword argument:
		gatewayConfigurationId -- ID of the gateway configuration to be used
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/subscriptions/" + quote_plus(self.id) + "/gateway-configurations/" + quote_plus(gatewayConfigurationId) + "/customer-action"
        data    = {

        }

        response = Response(request.get(path, data, options))
        body = response.body
        body = body["customer_action"]
        customerAction = CustomerAction(instance)
        return customerAction.fillWithData(body)
        
    def invoice(self, options = None):
        """Get the invoice corresponding to the last iteration of the subscription.
        Keyword argument:
		
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/subscriptions/" + quote_plus(self.id) + "/invoices"
        data    = {

        }

        response = Response(request.get(path, data, options))
        body = response.body
        body = body["invoice"]
        invoice = Invoice(instance)
        return invoice.fillWithData(body)
        
    def create(self, customerId, options = None):
        """Create a new subscription for the given customer.
        Keyword argument:
		customerId -- ID of the customer
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/subscriptions"
        data    = {
			'name': self.name, 
			'amount': self.amount, 
			'currency': self.currency, 
			'metadata': self.metadata, 
			'return_url': self.returnUrl, 
			'cancel_url': self.cancelUrl, 
			'interval': self.interval, 
			'trial_period': self.trialPeriod, 
			'ended_reason': self.endedReason, 
			'customer_id': customerId
        }

        response = Response(request.post(path, data, options))
        body = response.body
        body = body["subscription"]
        return self.fillWithData(body)
        
    @staticmethod
    def find(subscriptionId, options = None):
        """Find a subscription by its ID.
        Keyword argument:
		subscriptionId -- ID of the subscription
        options -- Options for the request"""
        instance = ProcessOut.getDefault()
        request = RequestProcessoutPrivate(instance)
        path    = "/subscriptions/" + quote_plus(subscriptionId) + ""
        data    = {

        }

        response = Response(request.get(path, data, options))
        body = response.body
        body = body["subscription"]
        obj = Subscription()
        return obj.fillWithData(body)
        
    def activate(self, source, options = None):
        """Activate the subscription with the provided token.
        Keyword argument:
		source -- Source to activate the subscription, such as a token
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/subscriptions/" + quote_plus(self.id) + ""
        data    = {
			'source': source
        }

        response = Response(request.put(path, data, options))
        return response.success
        
    def end(self, reason, options = None):
        """End a subscription. The reason may be provided as well.
        Keyword argument:
		reason -- Ending reason
        options -- Options for the request"""
        instance = self._instance
        request = RequestProcessoutPrivate(instance)
        path    = "/subscriptions/" + quote_plus(self.id) + ""
        data    = {
			'reason': reason
        }

        response = Response(request.delete(path, data, options))
        return response.success
        
    
