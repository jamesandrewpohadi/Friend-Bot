def mod(a,b):
	res = a % b
	text = str(a) + " mod " + str(b) + " = " + str(res)
	return {
		"speech": text
	}

def processP_Check(req):
    n = int(req.get("result").get("parameters").get("number"))
    r = int(n**(1/2))
    if n < 2:
        return {
            "speech": str(n) + " is not a prime number!" 
        }
    for i in range(2,r+1):
        if n % i == 0:
            return {
                "speech": str(n) + " is not a prime number!"
            }
    return {
        "speech": str(n) + " is a prime number!"
    }
	
