from os import environ, popen
from pyrogram import Client, filters
from pyrogram.types import Message
import random, math, requests


bot = Client(
    ':D3NV3ERxD:',
    api_id=environ['API_ID'],
    api_hash=environ['API_HASH'],
    bot_token=environ['TOKEN']
    )



def ccgen(prefix, ln):
    ccnumber = prefix
    while (len(ccnumber)<ln-1):
        ccnumber+=str(random.randint(0,9))
        
    sum=0
    pos=0
    reversedCCnumber=ccnumber[::-1]
    
    while (pos<ln-1):
        odd=reversedCCnumber[pos]*2
        if int(odd) > 9:
            odd =int(odd) - 9
        sum += int(odd)
        
        if pos != length - 2:
            sum += int(reversedCCnumber[ pos +1 ])
        pos += 2
        
    checkdigit = (( math.floor(sum/10) + 1) * 10 - sum) % 10
    ccnumber += str(checkdigit)
    
    return ccnumber
    
def credit_card_number(prefix, ln, howMany):
    result=[]
    for i in range(howMany):
        ccnumber = prefix
        result.append(ccgen(ccnumber, ln))
    return result
    
#print(credit_card_number(bin, 16, 10))

def rnDate(howMany):
    date=[]
    for i in range(1,30):
        date.append(i)
    rndate=[]
    for i in range(howMany):
        rndate.append(str(random.choice(date)))
    return rndate
      
#print(rnDate(10))


def rnYear(howMany):
    year=[]
    for i in range(2023, 2029):
        year.append(i)
    rnyear=[]
    for i in range(howMany):
        rnyear.append(str(random.choice(year)))
    return rnyear   
#print(rnYear(10))


def rnCVV(howMany):
    cvv=[]
    for i in range(100, 999):
       cvv.append(i)
    rncvv=[]
    for i in range(howMany):
        rncvv.append(str(random.choice(cvv)))
    
    return rncvv

#print(rnCVV(10))


def pipecc(prefix,ln,howMany):
    ccnum = credit_card_number(prefix, ln, howMany)
    year = rnYear(howMany)
    mon = rnDate(howMany)
    cvv = rnCVV(howMany)
    d=[]
    for i in range(0,howMany-1):
        d.append(ccnum[i]+"|"+mon[i]+"|"+year[i]+"|"+cvv[i])
        
    return list(d)   
def luhn(ccn):
    c = [int(x) for x in ccn[::-2]] 
    u2 = [(2*int(y))//10+(2*int(y))%10 for y in ccn[-2::-2]]
    return sum(c+u2)%10 == 0
def cccheck(cc):
    valid=[]
    nvalid=[]
    l=cc.split('\n')
    for i in l:
        t=i.split('|')[0]
        if luhn(t):
            valid.append(i)
        else:
            nvalid.append(i)
    return valid, nvalid
        
#print(pipecc("222222",16,10))

@bot.on_message(filters.command("start"))
async def start(client, message):
    message.reply_text(f"Hey 👋,\nI can help you generate Credit Card with BIN/n **Need Help?** /help")

@bot.on_message(filters.command("help"))
async def helpbot(client, message):
    message.reply_text(f"Hey 👋,\nI can help you generate Credit Card with BIN/n**Command Format :** `/gen {AMOUNT} {BIN}` \n\n__Dev :__ @D3NV3RxD")

@bot.on_message(filters.command("gen"))
async def ccgenbot(client, message):
    l = message.text.split()
    amt = l[1]
    bin = l[2]
    bin=bin.replace('x','')
    data = pipecc(bin, 16, int(amt))
    msg=""
    for cc in data:
        msg+=f"`{cc}`"+"\n"
        message.reply_text(f"**CC**/n{msg}/n/n**Dev :** @@D3NV3RxD")

@bot.on_message(filters.command("cccheck"))
async def cccheckbot(client, message):
    if message.reply_to_message:
        t=message.reply_to_message.text
    else:
        bot.send_message("**Reply to a Message!**")
    v, nv=cccheck(t)
    vmsg=""
    if len(v)!=0:
        for i in v:
            vmsg+=f"`{i}`"+"\n"
    nvmsg=""
    if len(nv)!=0:
        for i in nv:
            nvmsg+=f"`{i}`"+"\n"
    msg=""
    if vmsg!="":
        msg+=f"**VALID** __{len(v)}__\n{vmsg}\n"
    if nvmsg!="":
        msg+=f"**NOT VALID** __{len(nv)}__\n{nvmsg}\n"
    msg+="\n**Dev :** @D3NV3ERxD"
    bot.send_message(msg)
    
    
bot.run()