import redis
import uuid

r = redis.Redis(host='localhost', port=5000, db=0)

def acquire_lock(key, timeout = 5):
    l_id = str(uuid.uuid4())
    success = r.set(key, l_id, nx=True, ex=timeout)
    return l_id if success else None

def release_lock(key, l_id):
    store = r.get(key)
    if store == l_id:
        r.delete(key)
        return True
    return False