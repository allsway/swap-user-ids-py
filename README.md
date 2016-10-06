# swap-user-ids-py
Switches user primary ID with university ID in python

####swapids.py
Takes as arguments:
   - offset value
   - total number of patrons that should be updated on that call
   - swapids.txt
   
####swapids.txt
```
[Params]
apikey: apikey 
baseurl: host
campuscode: campuscode
id_type_to_swap: idcode
new_id_type: newidcode

```

Single run as 
`python ./swapids.py {offset} {total number of patrons you want to update} swapids.txt`

#####status.log
Logs all successful ID swaps, and failures due to validiation of the data and response codes from the Alma API
 
