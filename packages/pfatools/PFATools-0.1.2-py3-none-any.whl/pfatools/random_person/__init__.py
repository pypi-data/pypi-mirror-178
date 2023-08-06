import requests

class RandomUser:  
    def __init__(self, amount:int, defer=False):
        """RandomUser constructor for the RandomUser class.

        Args:
            amount (int): amount of users to get
            defer (bool, optional): whether to defer request. Defaults to False.

        Raises:
            ValueError: if amount is less than 1
        """        
        if amount <= 0: 
            raise ValueError('Amount must be greater than 0')
        elif amount > 1:
            self.url = f'https://randomuser.me/api/?results={amount}'
        self.url = "https://randomuser.me/api/"
        if not defer:
            self.data = self.run_query()
        else: 
            self.data = None
        

    def run_query(self): 
        response = requests.get(self.url)
        return response.json()