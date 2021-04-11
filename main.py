import amanobot
import amanobot.namedtuple
from amanobot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from amanobot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ForceReply
import random
import time
import os
import json
from glob import glob
import pytz
from datetime import datetime

token = "1626343681:AAGlz-7HOLcI0HCF4L3UvI1Wno-SqJ4lm2w"
bot = amanobot.Bot(token)

queue = {
	"free":[],
	"occupied":{}
}
users = []

def saveConfig(data):
	return open('config.json', 'w').write(json.dumps(data))

if __name__ == '__main__':
	s = time.time()
	print('[#] Buatan\n[i] Created by Davi ALFajr\n')
	print('[#] mengecek config...')
	if not os.path.isfile('config.json'):
		print('[#] memebuat config file...')
		open('config.json', 'w').write('{}')
		print('[#] Done')
	else:
		print('[#] Config found!')
	print('[i] Bot online ' + str(time.time() - s) + 's')
def exList(list, par):
	a = list
	a.remove(par)
	return a

def handle(update):
		
	global queue
	try:
		config = json.loads(open('config.json', 'r').read())
		if 'text' in update:
			text = update["text"]
		else:
			text = ""
		uid = update["from"]["id"]
		if uid not in users:
			users.append(uid)

		if not uid in config and text != "/nopics":
			config[str(uid)] = {"pics":True}
			saveConfig(config)

		if uid in queue["occupied"]:
			if 'text' in update:
				if text != "/key" and text != "❌ Exit" and text != "Next ▶️" and text != "Hapus Keyboard":
					bot.sendMessage(queue["occupied"][uid], "" + text)
			
			if 'photo' in update:
				if config[str(queue["occupied"][uid])]["pics"]:
					photo = update['photo'][0]['file_id']
					bot.sendPhoto(queue["occupied"][uid], photo)
				else:
					bot.sendMessage(queue["occupied"][uid], "Stranger tried to send you a photo, but you disabled this,  you can enable photos by using the /nopics command")
					bot.sendMessage(uid, "Stranger disabled photos, and will not receive your photos")

			if 'video' in update:
				video = update['video']['file_id']
				bot.sendVideo(queue["occupied"][uid], video)
				
			if 'voice' in update:
				voice = update['voice']['file_id']
				bot.sendVoice(queue["occupied"][uid], voice)

			if 'Video_Note' in update:
				VideoNote = update['Video_Note']['file_id']
				bot.sendVideoNote(queue["occupied"][uid], VideoNote)

			if 'sticker' in update:
				sticker = update['sticker']['file_id']
				bot.sendDocument(queue["occupied"][uid], sticker)


		if text == "/start":
			if not uid in queue["occupied"]:
				keyboard = ReplyKeyboardMarkup(keyboard=[['Cari 👥', 'Info Profile 📌'], ['Total Pengguna👤'],['New✅']], resize_keyboard=True)
				bot.sendMessage(uid, "*Selamat Bergabung Di Bot AnonymousMyBoo🙊*\n\n_Semoga Dapat teman atau jodoh, Dan selamat menunaikan ibadah puasa bagi yang menjalankan_\n\n*NOTE:*\nWAJIB JOIN [GRUP](t.me/caritemanh) > [CHANNEL](t.me/haluituenakkkk) DAN FOLLOW [INSTAGRAM](https://instagram.com/botmyboo2)", parse_mode='MarkDown', disable_web_page_preview=True , reply_markup=keyboard)

		if text == "/test":
			if not uid in queue["occupied"]:
				lolt = ReplyKeyboardMarkup(keyboard=[
                    ['Plain text', KeyboardButton(text='Text only')],
					[dict(text='phone', request_contact=True), KeyboardButton(text='Location', request_location=True)]], resize_keyboard=True)
				bot.sendMessage(uid, "contoh", reply_markup=lolt)

		elif text == "Total Pengguna👤":
			file = json.loads(open("config.json", "r").read())
			text = "Jumlah User Saat Ini : " + str(len(file)) + " User👤"
			bot.sendMessage(uid, text)

		elif text == 'Info Profile 📌':
			if "username" not in update["from"]:
				return bot.sendMessage(uid, "Harap Isi Username Kamu!!")
			if "last_name" not in update["from"]:
				return bot.sendMessage(uid, "Harap Isi Nama Belakang Kamu!!")
			if update["from"]["last_name"] != None:
				name = update["from"]["first_name"] + " " + update["from"]["last_name"]
				_id = update["from"]["id"]
				username = update["from"]["username"]
				tipe = update["chat"]["type"]
				date1 = datetime.fromtimestamp(update["date"], tz=pytz.timezone("asia/jakarta")).strftime("%d/%m/%Y %H:%M:%S").split()
				text = "*Nama : " + str(name)+"*" +"\n"
				text += "*ID Kamu :* " +"`"+ str(_id) +"`"+"\n"
				text += "*Username :* @" + str(username) + "\n"
				text += "*Tipe Chat* : " +"_"+ str(tipe)+"_" +"\n"
				text += "*Tanggal :* " + str(date1[0]) +"\n"
				text += "*Waktu :* " + str(date1[1]) + " WIB" "\n"
				bot.sendMessage(uid, text, parse_mode='MarkDown')

		elif text == 'Cari 👥':
			if not uid in queue["occupied"]:
				keyboard = ReplyKeyboardMarkup(keyboard=[
					['🔙 Main Menu']
				], resize_keyboard=True)
			bot.sendMessage(uid, '_Mencari pasangan halu kamu.. tunggu sebentar_',parse_mode='MarkDown', reply_markup=keyboard)
			print("[SB] " + str(uid) + " Join ke obrolan")
			queue["free"].append(uid)

		elif text == '❌ Exit' and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' meninggalkan jodohnya ' + str(queue["occupied"][uid]))
			keyboard = ReplyKeyboardMarkup(keyboard=[['Cari 👥', 'Info Profile 📌'], ['Total Pengguna👤'],['New✅']], resize_keyboard=True)
			bot.sendMessage(uid, "Obrolan telah berakhir")
			bot.sendMessage(uid, "*Selamat Bergabung Di Bot AnonymousMyBoo🙊*\n\n_Semoga Dapat teman atau jodoh, Dan selamat menunaikan ibadah puasa bagi yang menjalankan_\n\n*NOTE:*\nWAJIB JOIN [GRUP](t.me/caritemanh) > [CHANNEL](t.me/haluituenakkkk) DAN FOLLOW [INSTAGRAM](https://instagram.com/botmyboo2)", parse_mode='MarkDown', disable_web_page_preview=True, reply_markup=keyboard)
			bot.sendMessage(queue["occupied"][uid], "Pasangan kamu keluar dari obrolan", reply_markup=keyboard)
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid]

		elif text == 'New✅':
			keyboard = ReplyKeyboardMarkup(keyboard=[['Link Kejutan', 'Poto'],['🔙 Main Menu']], resize_keyboard=True)
			bot.sendMessage(uid, "Welcome My boo🙊\nYuk Join My Grup @caritemanh dan Channel @haluituenakkkk :)", reply_markup=keyboard)

		elif text == 'Link Kejutan':
			keyboard = ReplyKeyboardMarkup(keyboard=[['🔙 Main Menu']], resize_keyboard=True)
			bot.sendMessage(uid, 'Silahkan Klik Kejutan Dari aku by😙',reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="Kejutan 1😍", url='https://realsht.mobi/V3Mpf'), InlineKeyboardButton(text="Kejutan 2😍",url='https://realsht.mobi/A3Zmz')],
                                    [InlineKeyboardButton(text="Kejutan 3😍", url='https://realsht.mobi/o2XuR')]
                                ]
                            ))	
			bot.sendMessage(uid, "Thanks My Boo", reply_markup=keyboard)			

		elif text == '🔙 Main Menu':
			keyboard = ReplyKeyboardMarkup(keyboard=[['Cari 👥', 'Info Profile 📌'], ['Total Pengguna👤'],['New✅']], resize_keyboard=True)
			bot.sendMessage(uid, "*Selamat Bergabung Di Bot AnonymousMyBoo🙊*\n\n_Semoga Dapat teman atau jodoh, Dan selamat menunaikan ibadah puasa bagi yang menjalankan_\n\n*NOTE:*\nWAJIB JOIN [GRUP](t.me/caritemanh) > [CHANNEL](t.me/haluituenakkkk) DAN FOLLOW [INSTAGRAM](https://instagram.com/botmyboo2)", parse_mode='MarkDown', disable_web_page_preview=True, reply_markup=keyboard)

		elif text == 'Poto':
			picls = glob('*.jpg')
			love = random.choice(picls)
			with open(love, 'rb') as photo:
				bot.sendPhoto(uid, photo)

		elif text == "Next ▶️" and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' meninggalkan obrolan dengan ' + str(queue["occupied"][uid]))
			keyboard = ReplyKeyboardMarkup(keyboard=[['Cari 👥', '🔙 Main Menu']], resize_keyboard=True)
			bot.sendMessage(uid, "Mengakhiri obrolan...")
			bot.sendMessage(uid, "Obrolan telah berakhir")
			bot.sendMessage(queue["occupied"][uid], "Obrolan telah berakhir")
			bot.sendMessage(queue["occupied"][uid], "Pasangan kamu keluar dari obrolan")
			bot.sendMessage(queue["occupied"][uid], "tekan Cari untuk menemukan pasangan baru", reply_markup=keyboard)
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid] 
			if not uid in queue["occupied"]: 
				bot.sendMessage(uid, 'Mencari pasangan baru kamu.. tunggu sebentar')
				print("[SB] " + str(uid) + " Join ke obrolan") 
				queue["free"].append(uid)

		elif text == 'Hapus Keyboard':
			lolt1 = ReplyKeyboardRemove()
			bot.sendMessage(uid, 'Keyboard di Sembunyikan, klik /key untuk menampilkan keyboard', reply_markup=lolt1)

		if text == "/key":
				key = ReplyKeyboardMarkup(keyboard=[
					['Next ▶️', '❌ Exit'], ['Hapus Keyboard']
				], resize_keyboard=True)
				bot.sendMessage(uid, 'Keyboard Di tampilkan', reply_markup=key)
		
		if text == "/nopics":
			config[str(uid)]["pics"] = not config[str(uid)]["pics"] 
			if config[str(uid)]["pics"]:
				bot.sendMessage(uid, "Pasangan Mengirim Foto")
			else:
				bot.sendMessage(uid, "Pasangan Tidak Bisa Mengirim Fhoto")
			saveConfig(config)

		if len(queue["free"]) > 1 and not uid in queue["occupied"]:
			partner = random.choice(exList(queue["free"], uid))
			if partner != uid:
				keyboard = ReplyKeyboardMarkup(keyboard=[
					['Next ▶️', '❌ Exit'],['Hapus Keyboard']
				],resize_keyboard=True)
				print('[SB] ' + str(uid) + ' Berjodoh dengan ' + str(partner))
				queue["free"].remove(partner)
				queue["occupied"][uid] = partner
				queue["occupied"][partner] = uid
				bot.sendMessage(uid, '_Pasangan kamu telah ditemukan, selamat halu wkwk😜_',parse_mode='MarkDown', reply_markup=keyboard)
				bot.sendMessage(partner, '_Pasangan kamu telah ditemukann, selamat halu wkwk😜_',parse_mode='MarkDown', reply_markup=keyboard)
	except 	Exception as e:
		print('[!] Error: ' + str(e))

if __name__ == '__main__':
	bot.message_loop(handle)

	while True:
		time.sleep(10)
