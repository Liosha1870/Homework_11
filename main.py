from collections import UserDict
from datetime import datetime


class Field:                                
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
    

class Name(Field):                          
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.value
        
        
class Phone(Field):                         
    
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value
        
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone: str):
        new_phone = phone.strip()
        for char in '+( )-.':
            new_phone = new_phone.replace(char, "")
        if len(new_phone) >= 10 and new_phone.isdigit():
            new_phone = "+38" + new_phone[-10:]
        else:
            raise ValueError(f"{phone} - incorrect phone number")        
        self.__value = new_phone


class BirthDay(Field):                        #+++
    
    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, value):
        if value:
            self.__value = datetime.strptime(value, '%d-%m-%Y').date()


class Record:                               
    
    def __init__(self, name:Name, phone:Phone=None, birthday:BirthDay=None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
    
    def add_phone(self, phone:Phone=None):
        self.phones.append(phone)

    def remove_phone(self, phone:Phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
        
    def edit_phone(self, old_phone:Phone, new_phone:Phone):
        for i, p in enumerate(self.phones):
            if str(p)[-10:] == str(old_phone)[-10:]:
                self.phones[i] = new_phone
                return 
        raise ValueError(f"Number {old_phone} not found")  

    def find_phone(self, phone:Phone):
        for p in self.phones:
            if str(p)[-10:] == str(phone)[-10:]:
                return p
        # return None 
        return f"Number {phone} not found"
    
    def __str__(self) -> str:
        if self.birthday:
            return "{:<10} : {}   birthday: {} ({} days until the next)".format(self.name, (', '.join(str(p) for p in self.phones)), self.birthday, self.days_to_birthday(self.birthday))
        else:
            return "{:<10} : {} ".format(self.name, (', '.join(str(p) for p in self.phones)))
            
    def __repr__(self) -> str:
        return str(self)
    
    def days_to_birthday(self, birthday):
        today_date = datetime.today().date()
        bd_split = birthday.split('-')
        bd_this_year = datetime(day=int(bd_split[0]), month=int(bd_split[1]), year=today_date.year).date()
        bd_next_year = datetime(day=int(bd_split[0]), month=int(bd_split[1]), year=today_date.year+1).date()
        return ((bd_next_year - today_date) if (bd_this_year < today_date) else (bd_this_year - today_date)).days


class AddressBook(UserDict):            
    
    def add_record(self, record):
        self.data[record.name] = record
        
    def find(self, name:Name):
        return self.data.get(name)
    
    def delete(self, name):
            del self.data[name]
    
    def iterator(self, n=3):
        counter = 0
        while counter < len(self):
            yield list(self.values())[counter: counter + n]
            counter += n
