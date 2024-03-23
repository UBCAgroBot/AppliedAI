class EventManager:
    def __init__(self):
        print("Event Manager: Let me talk to the folks\n")
    
    def arrange(self):
        self.hotelier = Hotelier()
        self.hotelier.bookHotel()
        
        self.florist = Florist()
        self.florist.setFlowerRequirements()
        
        self.caterer = Caterer()
        self.caterer.setCuisine()
        
        self.musician = Musician()
        self.musician.setMusicType()


class Hotelier:
    def __init__(self):
        print("Arranging the Hotel for Marriage? --")
    
    def __isAvailable(self):
        print("Is the Hotel free for the event on given day?")
        return True
    
    def bookHotel(self):
        if self.__isAvailable():
            print("Registered the Booking\n")


class Florist:
    def __init__(self):
        print("Flower Decorations for the Event? --")
    
    def setFlowerRequirements(self):
        print("Carnations, Roses and Lilies would be used for Decorations\n")


class Caterer:
    def __init__(self):
        print("Food Arrangements for the Event --")
    
    def setCuisine(self):
        print("Chinese & Continental Cuisine to be served\n")


class Musician:
    def __init__(self):
        print("Musical Arrangements for the Marriage --")
    
    def setMusicType(self):
        print("Jazz and Classical will be played\n")

    
class Client:
    def __init__(self):
        print("Client: Whoa! My best friend is getting married!")
    def askEventManager(self):
        print("Client: Let's Contact the Event Manager\n")
        em = EventManager()
        em.arrange()
    def __del__(self):
        print("Client: Thanks to Event Manager, all preparations done! Phew!")


client = Client()
client.askEventManager()