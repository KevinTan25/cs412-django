from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
quote = [
    "Sometimes life hits you in the head with a brick. Don't lose faith.",
    "You can't connect the dots looking forward; you can only connect them looking backwards. So you have to trust that the dots will somehow connect in your future. You have to trust in something - your gut, destiny, life, karma, whatever. This approach has never let me down, and it has made all the difference in my life.",
    "Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma - which is living with the results of other people's thinking.",
] # List of quotes

images = [
    "https://photos5.appleinsider.com/gallery/product_pages/189-hero.jpg",
    "https://i.insider.com/656e93d10ec98e92f74c0510?width=700",
    "https://hips.hearstapps.com/hmg-prod/images/apple-ceo-steve-jobs-speaks-during-an-apple-special-event-news-photo-1683661736.jpg?crop=0.800xw:0.563xh;0.0657xw,0.0147xh&resize=1200:*",
] # List of images