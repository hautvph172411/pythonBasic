def sum(a , b):
  return a+b
# print("Tổng của 2 số là: ",sum(2,3))

def sumrange(a,b):
  total = 0
  for i in range(a,b+1):
    total += i
  return total
try: 
  a = int(input("Vui lòng nhập a: "))
  b = int(input("Vui lòng nhập b: "))
  if(a>=b):
    print("Vui lòng nhập a nhỏ hơn hoặc bằng b")
  else:
    print(f"Tổng các số từ {a} đến {b} là {sumrange(a,b)}")
except ValueError:
  print("Ký tự đầu vào không hợp lệ!!")

