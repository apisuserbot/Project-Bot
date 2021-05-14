import amanobot
import amanobot.namedtuple
from amanobot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from amanobot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ForceReply
import random
import requests
from bs4 import BeautifulSoup, NavigableString
import time
import os
import json
from glob import glob
import pytz
from datetime import datetime

token = "1626343681:AAH6zWFB1TnDoR6FmlFlqQNsgIRDP__C3qE"
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
				if text != "/next" and text != "❌ Exit" and text != "Next ▶️" and text != "/exit":
					bot.sendChatAction(queue["occupied"][uid], "typing")
					bot.sendMessage(queue["occupied"][uid], "" + text)
			
			if 'photo' in update:
				if config[str(queue["occupied"][uid])]["pics"]:
					photo = update['photo'][0]['file_id']
					bot.sendChatAction(queue["occupied"][uid], "upload_photo")
					bot.sendPhoto(queue["occupied"][uid], photo)
				else:
					bot.sendMessage(queue["occupied"][uid], "Stranger tried to send you a photo, but you disabled this,  you can enable photos by using the /nopics command")
					bot.sendMessage(uid, "Stranger disabled photos, and will not receive your photos")

			if 'video' in update:
				video = update['video']['file_id']
				bot.sendChatAction(queue["occupied"][uid], "upload_video")
				bot.sendVideo(queue["occupied"][uid], video)
				
			if 'document' in update:
				document = update['document']['file_id']
				bot.sendChatAction(queue["occupied"][uid], "upload_document")
				bot.sendDocument(queue["occupied"][uid], document)
				
			if 'audio' in update:
				audio = update['audio']['file_id']
				bot.sendChatAction(queue["occupied"][uid], "upload_voice")
				bot.sendAudio(queue["occupied"][uid], audio)
				
			if 'video_note' in update:
				video_note = update['video_note']['file_id']
				bot.sendChatAction(queue["occupied"][uid], "record_video_note")
				bot.sendVideoNote(queue["occupied"][uid], video_note)
			
			if 'voice' in update:
				voice = update['voice']['file_id']
				bot.sendChatAction(queue["occupied"][uid], "record_voice")
				bot.sendVoice(queue["occupied"][uid], voice)

			if 'sticker' in update:
				sticker = update['sticker']['file_id']
				bot.sendDocument(queue["occupied"][uid], sticker)


		if text == "/start" or text == "/refresh":
			if not uid in queue["occupied"]:
				keyboard = ReplyKeyboardMarkup(keyboard=[['Search 🔍'],['Pengguna👤','MENU BOT✅'],['BAGI BAGI THR GRATIS✅']], resize_keyboard=True, one_time_keyboard=True)
				bot.sendMessage(uid, "*Selamat Bergabung Di Bot AnonymousMyBoo🙊*\n\n_🇮🇩 Semoga Dapat teman atau jodoh\n🇳🇿 I hope you can make a friend or a partner_\n\n*NOTE:*\nWAJIB JOIN [GRUP](t.me/caritemanh) > [CHANNEL](t.me/haluituenakkkk) DAN FOLLOW [INSTAGRAM](https://instagram.com/botmyboo2) > [YOUTUBE](https://www.youtube.com/channel/UCE6TQ4yG8eNEiOzqRSfOu-w)", parse_mode='MarkDown', disable_web_page_preview=True , reply_markup=keyboard)

		if text == "/test":
			if not uid in queue["occupied"]:
				lolt = ReplyKeyboardMarkup(keyboard=[
                    ['Plain text', KeyboardButton(text='Text only')],
					[dict(text='phone', request_contact=True), KeyboardButton(text='Location', request_location=True)]], resize_keyboard=True)
				bot.sendMessage(uid, "contoh", reply_markup=lolt)

		elif text == "Pengguna👤":
			file = json.loads(open("config.json", "r").read())
			text = "Pengguna Online Saat Ini : " + str(len(file)) + " Online👤"
			bot.sendMessage(uid, text)

		elif text == "BAGI BAGI THR GRATIS✅":
			if not uid in queue["occupied"]:
				bot.sendMessage(uid, "Mohon tunggu sebentar...")
				bot.sendChatAction(uid, "upload_video")
				bot.sendVideo(uid, video=open('iklan/gratis.mp4','rb'),
				caption='THR GRATIS KHUSUS BUAT PENGGUNA YANG BELUM PERNAH INSTAL TIKTOK LITE\n\n> Instal Tiktok Lite (Khusus Pengguna Baru)\n> Masukkan Kode Berikut *A5807808469*\n> Selamat Saldo Anda Sudah Masuk', parse_mode="MarkDown", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
					[InlineKeyboardButton(text="DAPATKAN THR GRATIS", url="https://play.google.com/store/apps/details?id=com.zhiliaoapp.musically.go")]
				]))

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

		elif text == 'Search 🔍':
			if not uid in queue["occupied"]:
				keyboard = ReplyKeyboardRemove()
				bot.sendMessage(uid, '_Mencari pasangan halu kamu.. tunggu sebentar_',parse_mode='MarkDown', reply_markup=keyboard)
				print("[SB] " + str(uid) + " Join ke obrolan")
				queue["free"].append(uid)

		elif text == '❌ Exit' or text == '/exit' and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' meninggalkan jodohnya ' + str(queue["occupied"][uid]))
			keyboard = ReplyKeyboardMarkup(keyboard=[['Search 🔍'],['Pengguna👤','MENU BOT✅'],['BAGI BAGI THR GRATIS✅']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "Obrolan telah berakhir")
			bot.sendMessage(uid, "*Selamat Bergabung Di Bot AnonymousMyBoo🙊*\n\n_🇮🇩 Semoga Dapat teman atau jodoh\n🇳🇿 I hope you can make a friend or a partner_\n\n*NOTE:*\nWAJIB JOIN [GRUP](t.me/caritemanh) > [CHANNEL](t.me/haluituenakkkk) DAN FOLLOW [INSTAGRAM](https://instagram.com/botmyboo2) > [YOUTUBE](https://www.youtube.com/channel/UCE6TQ4yG8eNEiOzqRSfOu-w)", parse_mode='MarkDown', disable_web_page_preview=True, reply_markup=keyboard)
			bot.sendMessage(queue["occupied"][uid], "Pasangan kamu keluar dari obrolan", reply_markup=keyboard)
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid]

		elif text == 'MENU BOT✅':
			keyboard = ReplyKeyboardMarkup(keyboard=[
				['Info Profile 📌'],['Link Kejutan', 'RandomPhoto📷'],['BAGI BAGI THR GRATIS✅'],['Covid-19〽️','Youtube▶️'],['🔙 Main Menu']
			], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "Welcome My boo🙊\nYuk Join My Grup @caritemanh dan Channel @haluituenakkkk :)", reply_markup=keyboard)

		elif text == 'Covid-19〽️':
			web = requests.get('https://www.worldometers.info/coronavirus/country/indonesia/')
			tampilan = BeautifulSoup(web.content, 'html.parser')
			dataweb = tampilan.find_all("div", {"class": "maincounter-number"})
			ouy = "*KASUS VIRUS COVID-19 DI INDONESIA 🇮🇩*\n\nTerpapar Virus : {} Orang\nMeninggal : {} Orang\nSembuh : {} Orang".format(dataweb[0].span.text,dataweb[1].span.text,dataweb[2].span.text)
			bot.sendMessage(uid, ouy, parse_mode='MarkDown')
			
		elif text == "Youtube▶️" or text == "/subscribe":
			bot.sendMessage(uid, 'Yuk Nonton Video Video aku, Cek di button keyboard', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text="SUBSCRIBE YOUTUBE", url='https://youtube.com/channel/UCE6TQ4yG8eNEiOzqRSfOu-w')],
				[InlineKeyboardButton(text="FILM PENDEK", url="https://youtu.be/35wJMkvSlQU" )],
				[InlineKeyboardButton(text="BOT JADWAL SHOLAT", url='https://youtu.be/YRcKu-kZd0o'), InlineKeyboardButton(text='NEW FITUR BOT', url='https://youtu.be/TKmSmDBLuos'), InlineKeyboardButton(text='DOWNLOAD VIDEO TIKTOK', url='https://youtu.be/P0iBcUAGuzE')],
				[InlineKeyboardButton(text=">>",url="https://youtu.be/YRcKu-kZd0o")]
			]))

		elif text == 'Link Kejutan':
			bot.sendMessage(uid, 'Silahkan Klik Kejutan Dari aku by😙',reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="Kejutan 1😍", url='https://realsht.mobi/V3Mpf'), InlineKeyboardButton(text="Kejutan 2😍",url='https://realsht.mobi/A3Zmz')],
                                    [InlineKeyboardButton(text="Kejutan 3😍", url='https://realsht.mobi/o2XuR')]
                                ]
                            ))	

		elif text == '🔙 Main Menu':
			keyboard = ReplyKeyboardMarkup(keyboard=[['Search 🔍'],['Pengguna👤','MENU BOT✅'],['BAGI BAGI THR GRATIS✅']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "*Selamat Bergabung Di Bot AnonymousMyBoo🙊*\n\n_🇮🇩 Semoga Dapat teman atau jodoh\n🇳🇿 I hope you can make a friend or a partner_\n\n*NOTE:*\nWAJIB JOIN [GRUP](t.me/caritemanh) > [CHANNEL](t.me/haluituenakkkk) DAN FOLLOW [INSTAGRAM](https://instagram.com/botmyboo2) > [YOUTUBE](https://www.youtube.com/channel/UCE6TQ4yG8eNEiOzqRSfOu-w)", parse_mode='MarkDown', disable_web_page_preview=True, reply_markup=keyboard)

		elif text == 'RandomPhoto📷':
			picls = glob("img/*.jpg")
			love = random.choice(picls)
			with open(love, 'rb') as photo:
				bot.sendPhoto(uid, photo)

		elif text == "Next ▶️" or text == "/next" and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' meninggalkan obrolan dengan ' + str(queue["occupied"][uid]))
			keyboard = ReplyKeyboardMarkup(keyboard=[['Search 🔍', '🔙 Main Menu']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "🛑 Obrolan telah berakhir!")
			bot.sendMessage(queue["occupied"][uid], "🛑 Obrolan telah berakhir!", reply_markup=keyboard)
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid] 
			if not uid in queue["occupied"]:
				key = ReplyKeyboardRemove()
				bot.sendMessage(uid, 'Mencari pasangan baru kamu.. tunggu sebentar',reply_markup=key)
				print("[SB] " + str(uid) + " Join ke obrolan") 
				queue["free"].append(uid)
		
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
					['Hii..','Cewe atau Cowo?','Umur Berapa?'],['Next ▶️', '❌ Exit']
				],resize_keyboard=True, one_time_keyboard=True)
				print('[SB] ' + str(uid) + ' Berjodoh dengan ' + str(partner))
				queue["free"].remove(partner)
				queue["occupied"][uid] = partner
				queue["occupied"][partner] = uid
				bot.sendMessage(uid, '_🎈Pasangan kamu telah ditemukan, selamat halu wkwk_',parse_mode='MarkDown', reply_markup=keyboard)
				bot.sendMessage(partner, '_🎈Pasangan kamu telah ditemukann, selamat halu wkwk_',parse_mode='MarkDown', reply_markup=keyboard)
	except 	Exception as e:
		print('[!] Error: ' + str(e))

if __name__ == '__main__':
	bot.message_loop(handle)

	while 1:
		time.sleep(3)
