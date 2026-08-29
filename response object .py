from dataclasses import dataclass
import urllib.request 
import urllib.error
import time 
@dataclass
class Response:
    status:int 
    header: dict 
    body:str 
    reason: str 
    elapse: float 
@classmethod 
def from_openurllib(cls,url:str):
    start=time.perf_counter()
    try:
        with urllib.request.urlopen(url) as response:
            #obtaining headers of the Response
            status=response.status 
            header = dict(response.getheaders())
            reason=response.reason
            #reading data from opened URL
            body= response.read().decode("utf-8")
            elapsed=time.perf_counter()-start 
            return cls(status=status, 
                       header=header, 
                       body=body,
                       elapse=elapsed,
                       reason=reason)
            
    except urllib.error.HTTPError as e:
        return cls(status=e.code,
                   reason=e.reason,
                   header=dict(e.headers.items()),
                   body=e.read().decode("utf-8"),
                   elapse=time.perf_counter()-start
                   )
        

