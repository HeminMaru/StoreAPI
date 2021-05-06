# StoreAPI
https://online-store-free-rest-api.herokuapp.com/


Endpoints:

1. To register: 
Post : /register

2. To login:
Post : /login

3. To create store :
Post : /stores/<ownerName>/<storeName>

4. To create item:
Post : /stores/<storeName>/items/<itemName>

5. Get store list :
Post : /stores

6. Get a particular store : 
Post : /stores/<ownerName>/storeName

7. Delete a particular store with all its items:
Delete : /stores/<ownerName>/storeName

8. Get list of items:
Get : /items

9. Get list of items of particular store :
Get : /stores/<storeName>/items

10. Get list of particular item :
Get : /items/<itemName>

11. Get a particular item from particular store :
Get : /stores/<storeName>/items/<itemName>

12. Update price of an item of a particular store :
Put : /stores/<storeName>/items/<itemName>

13. Delete a particular item:
Delete : /stores/<storeName>/items/<itemName>
