from abc import abstractmethod, ABC


class NuBankServiceBasicInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def authenticate(self,
                     token: str,
                     certificate_path: str):
        pass

    @abstractmethod
    def get_balance(self):
        pass


class NuBankServiceInterface:
    def __init__(self,
                 token: str,
                 certificate_path: str,
                 bank_service):
        self.token = token
        self.certificate_path = certificate_path
        self.bank_service = bank_service
        self.bank_service.authenticate(self.token, self.certificate_path)

    def get_balance(self):
        return self.bank_service.get_balance()

