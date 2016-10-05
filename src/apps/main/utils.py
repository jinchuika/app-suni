def get_telefonica(num_telefono):
	if(num_telefono < 30000000 or num_telefono >= 60000000):
		return "otro"

	if (((30000000<= num_telefono) and (num_telefono <= 33599999))
		or ((40000000<= num_telefono) and (num_telefono <= 40999999))
		or ((44760000<= num_telefono) and (num_telefono <= 46999999))
		or ((47730000<= num_telefono) and (num_telefono <= 48199999))
		or ((48220000<= num_telefono) and (num_telefono <= 50099999))
		or ((50300000<= num_telefono) and (num_telefono <= 50699999))
		or ((51500000<= num_telefono) and (num_telefono <= 52099999))
		or ((53000000<= num_telefono) and (num_telefono <= 53099999))
		or ((53140000<= num_telefono) and (num_telefono <= 53899999))
		or ((55200000<= num_telefono) and (num_telefono <= 55299999))
		or ((55500000<= num_telefono) and (num_telefono <= 55539999))
		or ((55800000<= num_telefono) and (num_telefono <= 55819999))
		or ((57000000<= num_telefono) and (num_telefono <= 57099999))
		or ((57190000<= num_telefono) and (num_telefono <= 57899999))
		or ((58000000<= num_telefono) and (num_telefono <= 58099999))
		or ((58190000<= num_telefono) and (num_telefono <= 58199999))
		or ((58800000<= num_telefono) and (num_telefono <= 59099999))
		or ((59180000<= num_telefono) and (num_telefono <= 59199999))
		or ((59900000<= num_telefono) and (num_telefono <= 59999999))):
		return "tigo"

	elif (((34000000<= num_telefono) and (num_telefono <=34699999))
		or ((43000000<= num_telefono) and (num_telefono <=44759999))
		or ((50200000<= num_telefono) and (num_telefono <=50299999))
		or ((50700000<= num_telefono) and (num_telefono <=51099999))
		or ((51400000<= num_telefono) and (num_telefono <=51499999))
		or ((52100000<= num_telefono) and (num_telefono <=52999999))
		or ((53120000<= num_telefono) and (num_telefono <=53139999))
		or ((53900000<= num_telefono) and (num_telefono <=54099999))
		or ((55000000<= num_telefono) and (num_telefono <=55099999))
		or ((55180000<= num_telefono) and (num_telefono <=55199999))
		or ((55400000<= num_telefono) and (num_telefono <=55429999))
		or ((55450000<= num_telefono) and (num_telefono <=55499999))
		or ((56000000<= num_telefono) and (num_telefono <=56099999))
		or ((56400000<= num_telefono) and (num_telefono <=56899999))
		or ((57900000<= num_telefono) and (num_telefono <=57999999))
		or ((59150000<= num_telefono) and (num_telefono <=59179999)) ):
		return "movistar"

	elif(((41000000<= num_telefono) and (num_telefono <=42999999))
		or ((47000000<= num_telefono) and (num_telefono <=47729999))
		or ((50100000<= num_telefono) and (num_telefono <=50199999))
		or ((51100000<= num_telefono) and (num_telefono <=51399999))
		or ((53100000<= num_telefono) and (num_telefono <=53119999))
		or ((54100000<= num_telefono) and (num_telefono <=54999999))
		or ((55100000<= num_telefono) and (num_telefono <=55179999))
		or ((55300000<= num_telefono) and (num_telefono <=55399999))
		or ((55430000<= num_telefono) and (num_telefono <=55449999))
		or ((55540000<= num_telefono) and (num_telefono <=55799999))
		or ((55820000<= num_telefono) and (num_telefono <=55999999))
		or ((56100000<= num_telefono) and (num_telefono <=56399999))
		or ((56900000<= num_telefono) and (num_telefono <=56999999))
		or ((57100000<= num_telefono) and (num_telefono <=57189999))
		or ((58100000<= num_telefono) and (num_telefono <=58189999))
		or ((58200000<= num_telefono) and (num_telefono <=58799999))
		or ((59100000<= num_telefono) and (num_telefono <=59149999))
		or ((59200000<= num_telefono) and (num_telefono <=59899999))):
		return "claro"

	else:
		return "otro"