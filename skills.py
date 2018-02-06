def euler(req):
    n = int(req.get("result").get("parameters").get("number"))
    x = 0
    for i in range(1,n):
        for b in range(2,i+1):
            if i%b == n%b == 0:
                x = x + 1
                break
    res = n-x-1
	return {
		"speech": "euler({}) = {}".format(n,res)
	}


def mod(req):
    a = int(req.get("result").get("parameters").get("number"))
	b = int(req.get("result").get("parameters").get("number1"))
	res = a%b
	return {
		"speech": str(a) + " mod " + str(b) + " = " + str(res)
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
	
