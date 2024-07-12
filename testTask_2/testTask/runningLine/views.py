import cv2
import numpy as np
import os
from django.http import HttpResponse
from django.utils.timezone import localtime, now
from .models import Request

def hello(requeste):
	return HttpResponse("Напишите в адресной строке Ваш текст после /")

def textGenerator(requeste, text):
	text = str(text)
	if text == "favicon.ico":
		return HttpResponse()
	infoBd = Request(userText = text, dateText = localtime(now()))#создаю объект модели Request
	infoBd.save()#cохраняю в БД
	# задаём параметры для отображения текста и записи видео
	ws_h = 400#высота видео в пикселях
	ws_w = 600#ширина видео в пикселях
	wh = ws_w/ws_h
	fps = 24.0#задаём количество кадров
	path_to_save = '/content/testTask_2'#путь сохранения видеофаййла
	video_path = os.path.join(path_to_save, "video" + ".mp4")#соединяет путь с именем файла
	font_face = cv2.FONT_HERSHEY_TRIPLEX#задание типа шрифта
	font_scale = 8.0#размер шрифта
	thickness = 8#толщина шрифта
	fourcc = cv2.VideoWriter.fourcc('m','p','4','v')#сохраняем файл с помощью видеокодека FourCC

	# определяем размеры и цвет фонового изображения (background image)
	(width, higth), _ = cv2.getTextSize(text, font_face, font_scale, thickness)#записываем размеры текста
	bg_w, bg_h = int(2*int(3*higth*wh) + width), int(3 * higth)#записываем размер фона
	bg_img = np.zeros((bg_h, bg_w, 3), np.uint8)#создание матрицы изображения
	bg_img[:,:,1] = 200 # заполняем матрицу в зелёный цвет [y , x]
	bg_img[:,:,0] = 53 # заполняем матрицу в синий цвет
	text_color = (255, 255, 255)#задаем цвет текста

	# накладываем текст на фоновое изображение и приводим к нужному размеру

	koef = ws_w / bg_w#коэффициент перевода 
	org = (int(3*higth*wh), int(2 * higth))#int(higth / 2)#задаем координаты левого нижнего угла текста на картинке
	img_w_text = cv2.putText(bg_img, text, org, font_face, font_scale, text_color, thickness)#рисуем строку текста на фоне 
	target_img = cv2.resize(img_w_text, (ws_h*bg_w//bg_h,ws_h))#изменяем размер картинки под наши нужды

	# создаём VideoWriter и записываем кадры
	time = 3#длительность видео в секундах
	num_frames = int(fps * time)#задаём количество кадров
	step = (ws_h*bg_w//bg_h - ws_w) // (num_frames + 1)#задаём сдвиг
	video = cv2.VideoWriter(video_path, fourcc, fps, (ws_w, ws_h))#создаём объект VideoWriter для записи видео
	
	#создаём цикл для покадровой записи
	print('WRiting ', text)
	print(width, higth, bg_w, bg_h, step,num_frames, ws_h*bg_w//bg_h, len(target_img[0]))
	for i in range(num_frames):
		window_start = int(step * i)#задаём шаг
		frame = target_img[:,window_start:window_start + ws_w]
		print(window_start + ws_w, i, len(frame[0]))
		video.write(frame)#записываем кадр
	video.release()#освобождаю объект
	
	return HttpResponse(f"""
			<h2>testTask</h2>
			<p>Ваш текст: {text}</p>
			""")#вывожу на экран текст пользователя, завершаю функцию
