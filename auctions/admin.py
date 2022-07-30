from django.contrib import admin
from .models import AuctionListing, Category, User, Bids,Comment


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('id','title','description','start_bid','current_bid','flActive','datetime','category','creator', 'buyer')

class BidsAdmin(admin.ModelAdmin):
    list_display = ('id','user','auction','bid','date')
    
    
class CommetAdmin(admin.ModelAdmin):
    list_display = ('id','user','auction','comment','createdDate')

admin.site.register(AuctionListing,AuctionListingAdmin)
admin.site.register(Bids,BidsAdmin)
admin.site.register(Comment,CommetAdmin)
admin.site.register(Category)