import telepot
import random
import time
import os
import json

token = "1626343681:AAGLoexvHzVkmXBbzKQhXoEuTLuNw21fHiU"
bot = telepot.Bot(token)

queue = {
	"free":[],
	"occupied":{}
}

def saveConfig(data):
	return open('config.json', 'w').write(json.dumps(data))

if __name__ == '__main__':
	s = time.time()
	print('[#] Swirlbot 2\n[i] Created by TheFamilyTeam - @TheFamilyTeam\n')
	print('[#] Checking config...')
	if not os.path.isfile('config.json'):
		print('[#] Creating config file...')
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

		if not uid in config and text != "/nopics":
			config[str(uid)] = {"pics":True}
			saveConfig(config)

		if uid in queue["occupied"]:
			if 'text' in update:
				if text != "/end":
					bot.sendMessage(queue["occupied"][uid], "Sihalu: " + text)
			
			if 'photo' in update:
				if config[str(queue["occupied"][uid])]["pics"]:
					photo = update['photo'][0]['file_id']
					bot.sendPhoto(queue["occupied"][uid], photo)
					bot.sendMessage(queue["occupied"][uid], "sihalu mengirim kamu foto")
				else:
					bot.sendMessage(queue["occupied"][uid], "Stranger tried to send you a photo, but you disabled this,  you can enable photos by using the /nopics command")
					bot.sendMessage(uid, "Stranger disabled photos, and will not receive your photos")

			if 'video' in update:
				video = update['video']['file_id']
				bot.sendVideo(queue["occupied"][uid], video)
				bot.sendMessage(queue["occupied"][uid], "Sihalu mengirim kamu video")

			if 'sticker' in update:
				sticker = update['sticker']['file_id']
				bot.sendDocument(queue["occupied"][uid], sticker)
				bot.sendMessage(queue["occupied"][uid], "Sihalu Mengirim stiker")

		if text == "/end" and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' left the conversation with ' + str(queue["occupied"][uid]))
			bot.sendMessage(uid, "Kamu Mengakhiri Obrolan:)")
			bot.sendMessage(uid, "Tekan /start Untuk Mencari pasangan Baru")
			bot.sendMessage(uid, "Yuk Halu Lagi")
			bot.sendMessage(queue["occupied"][uid], "Obrolan Telah Berakhir")
			bot.sendMessage(queue["occupied"][uid], "Yah Pasangan Halu Kamu mengakhiri obrolan, Jangan Sedih ya:)")
			bot.sendMessage(queue["occupied"][uid], "Tekan /start untuk menemukan pasangan baru")
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid]

		if text == "/start":
			if not uid in queue["occupied"]:
				bot.sendMessage(uid, 'Mencari pasangan halu kamu.. tunggu sebentar')
				print("[SB] " + str(uid) + " joined the queue")
				queue["free"].append(uid)
				
		if text == "/next" and uid in queue["occupied"]: 
			print('[SB] ' + str(uid) + ' meninggalkan obrolan dengan ' + str(queue["occupied"][uid]))
			bot.sendMessage(uid, "Mengakhiri obrolan...")
			bot.sendMessage(uid, "Obrolan telah berakhir")
			bot.sendMessage(queue["occupied"][uid], "Obrolan telah berakhir")
			bot.sendMessage(queue["occupied"][uid], "Pasangan kamu keluar dari obrolan")
			bot.sendMessage(queue["occupied"][uid], "tekan /start untuk menemukan pasangan baru")
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid] if not uid in queue["occupied"]: 
				bot.sendMessage(uid, 'Mencari pasangan baru kamu.. tunggu sebentar')
				print("[SB] " + str(uid) + " joined the queue") 
				queue["free"].append(uid)		
		

		if text == "/help":
			bot.sendMessage(uid, "Help:\n\nGunakan /start untuk mencari pasangan kamu,Jika ingin mencari pasangan baru tekan /next , dan jika ingin mengakhiri obrolan tekan /end .\n\n Jangan Lupa join grup @caritemanh")

		if text == "/nopics":
			config[str(uid)]["pics"] = not config[str(uid)]["pics"] 
			if config[str(uid)]["pics"]:
				bot.sendMessage(uid, "Sihalu Mengirim Foto")
			else:
				bot.sendMessage(uid, "Sihalu Tidak Bisa Mengirim Fhoto")
			saveConfig(config)

		if len(queue["free"]) > 1 and not uid in queue["occupied"]:
			partner = random.choice(exList(queue["free"], uid))
			if partner != uid:
				print('[SB] ' + str(uid) + ' matched with ' + str(partner))
				queue["free"].remove(partner)
				queue["occupied"][uid] = partner
				queue["occupied"][partner] = uid
				bot.sendMessage(uid, 'Pasangan kamu telah ditemukan, selamat halu wkwk')
				bot.sendMessage(partner, 'Pasangan kamu telah ditemukan, selamat halu wkwk')
	except 	Exception as e:
		print('[!] Error: ' + str(e))

if __name__ == '__main__':
	bot.message_loop(handle)

	while True:
		time.sleep(10)
