import tkinter
from tkinter import *
from tkinter import messagebox
import base64


window = Tk()
window.title("Top secret")
window.geometry("400x700")

top_secret_png = PhotoImage(file="top_secret.png")
top_secret_png =top_secret_png.subsample(5,5)
png_label = Label(window, image=top_secret_png)
png_label.pack()




def file_creat():
  file_name = file_entry.get()
  file_text = text_text.get(1.0, END).strip()
  master_key = master_key_entry.get()


  if file_name == "" or file_text == "" or master_key == "":
    messagebox.showerror(title="Hata", message="Bütün değerleri giriniz")
    return

  else:
      text_bytes = file_text.encode("utf-8")
      key_bytes = master_key.encode("utf-8")
      secret_bytes=bytearray()
      for i in range(len(text_bytes)):
          key_byte = key_bytes[i % len(key_bytes)]
          secret_bytes.append(text_bytes[i] ^ key_byte)

      with open("User_Notes.txt", "a", encoding="utf-8") as file:
        file.write(file_name + "\n")
        file.write(base64.b64encode(secret_bytes).decode("utf-8") + "\n\n")


      file_entry.delete(0, END)
      master_key_entry.delete(0, END)
      text_text.delete(index1="1.0", index2=END)
      messagebox.showinfo(title="Başarılı", message="Dosyanız başarıyla kaydedildi")




def decode_text():
    decode_master_key = master_key_entry.get()
    encrypted_text = text_text.get(1.0, END).strip()
    if decode_master_key == "" or encrypted_text == "":
        messagebox.showerror(title="Hata",message= "Şifrenizi ve gizlenmiş metninizi giriniz")
        return

    try:
        secret_bytes = base64.b64decode(encrypted_text)
        key_bytes = decode_master_key.encode("utf-8")
        decrypted_bytes = bytearray()
        for i in range(len(secret_bytes)):
            key_byte = key_bytes[i % len(key_bytes)]
            decrypted_bytes.append(secret_bytes[i] ^ key_byte)
        decoded_text = decrypted_bytes.decode("utf-8")
        text_text.delete(1.0, END)
        text_text.insert(1.0, decoded_text)

    except Exception:
        messagebox.showerror(title="Hata",message="Şifreniz hatalıdır")



#ui
file_label = tkinter.Label(text="Dosya adını giriniz")
file_label.pack()
file_entry = tkinter.Entry()
file_entry.config(width=35)
file_entry.pack()
text_label = tkinter.Label(text="Gizlemek istediğiniz metini yazınız")
text_label.pack()
text_text = tkinter.Text(width=35,height=15)
text_text.pack()
master_key_label = tkinter.Label(text = "Şifrenizi giriniz")
master_key_label.pack()
master_key_entry = tkinter.Entry()
master_key_entry.config(width=35)
master_key_entry.pack()
save_button = tkinter.Button(text="Kaydet & Şifrele",command=file_creat)
save_button.pack()
decrypt_button = tkinter.Button(text="Metni çöz",command=decode_text)
decrypt_button.pack()



window.mainloop()

