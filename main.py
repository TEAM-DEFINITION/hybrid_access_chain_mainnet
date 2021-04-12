from fastapi import FastAPI,Request,Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json

from blockchain_main import Blockchain

# http://112.156.0.196:55555
# Fastapi function start
app = FastAPI()

# CORS Setting
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# static management
#app.mount("/static", StaticFiles(directory='static'), name='static')
#templates = Jinja2Templates(directory='templates')

from uuid import uuid4


# Blockchain Network API Management
@app.get('/mine')
def mine():
    # 트랙젝션 발생확인
    if len(Blockchain.current_transaction) == 0:
        return "Any transaction", 200

    # We run the proof of work algorithm to get the next proof...
    last_block = Blockchain().last_block
    last_proof = last_block['proof']
    proof = Blockchain().proof_of_work(last_proof)

    # 블록 채굴에 대한 보상을 설정한다.
    # 송신자를 0으로 표현한 것은 블록 채굴에 대한 보상이기 때문이다.
    Blockchain().new_transaction(
        sender="0",
        recipient= str(uuid4()).replace('-', ''),
        amount=1,
    )

    # 체인에 새로운 블록을 추가하는 코드이다. 
    previous_hash = Blockchain().hash(last_block)
    block = Blockchain().new_block(proof, previous_hash)

    if block == 0:
        return "Any transaction", 200
    
    else :
        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'prev_hash': block['prev_hash'],
        }
    Blockchain().clear_transaction()
    return json.dumps(response), 200

@app.get('/chain')
def full_chain(request):
    result = Blockchain().show_chain()
    return result, 200

@app.post('/transaction/new')
def new_transaction(sender, recipient, amount):

    # 새로운 거래를 추가
    index = Blockchain().new_transaction(sender, recipient, amount)
    response = {'message': f'Transaction Will be added to Block {index}'}
    return json.dumps(response), 200

########################################################################################

# 자동 시작
if __name__== "__main__":
    Blockchain().genesis_block()
    uvicorn.run("main:app", host="0.0.0.0", port=55556, reload=True)
    