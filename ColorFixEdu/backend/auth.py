from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Şifreleme ve JWT ayarları
SECRET_KEY = "your_secret_key"  # Bu anahtarı güvenli bir şekilde saklayın
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Kullanıcı modeli
class User(BaseModel):
    username: str
    password: str

# Basit bir kullanıcı veritabanı simülasyonu
fake_users_db = {}

# Şifre doğrulama ve oluşturma fonksiyonları
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Kullanıcı doğrulama fonksiyonu
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        return None
    return user

# JWT token oluşturma fonksiyonu
def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        print(f"Creating token with data: {to_encode}")  # Hata ayıklama için log ekledim
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        print(f"Token creation error: {e}")  # Hata durumunda log ekledim
        raise

# Kullanıcı kaydı endpoint'i
@app.post("/register")
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Kullanıcı zaten mevcut!")
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {"username": user.username, "password": hashed_password}
    return {"message": "Kullanıcı başarıyla oluşturuldu!"}

# Kullanıcı giriş endpoint'inde hata kontrolünü iyileştiriyorum
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            print(f"Login failed: Invalid username or password for username: {form_data.username}")  # Hata logu ekledim
            raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre!")
        access_token = create_access_token(data={"sub": user["username"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e  # HTTPException'ı olduğu gibi döndürüyorum
    except Exception as e:
        print(f"Unexpected login error: {e}")  # Beklenmeyen hatalar için log ekledim
        raise HTTPException(status_code=500, detail="Sunucu hatası")

# Korunan bir endpoint örneği
@app.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Geçersiz token!")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token süresi dolmuş!")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token!")

    return {"message": f"Hoş geldin {username}!"}

# Test için basit bir JWT oluşturma fonksiyonu ekliyorum
@app.get("/test-token")
async def test_token():
    try:
        test_data = {"sub": "test_user", "exp": datetime.utcnow() + timedelta(minutes=5)}
        print(f"Test token data: {test_data}")
        token = jwt.encode(test_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"test_token": token}
    except Exception as e:
        print(f"Test token creation error: {e}")
        raise HTTPException(status_code=500, detail="Test token oluşturulamadı")

# CORS ayarlarını ekleyin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm domainlere izin verir, güvenlik için sadece frontend URL'sini ekleyin, örn: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/auth/login")
async def login(request: LoginRequest):
    # Kullanıcı doğrulama işlemi burada yapılır
    if request.username == "admin" and request.password == "1234":
        return {"message": "Giriş başarılı!", "username": request.username}
    else:
        return {"message": "Geçersiz kullanıcı adı veya şifre"}, 401
