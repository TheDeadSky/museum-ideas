import vk_api
import requests

# Авторизация через токен группы
vk_session = vk_api.VkApi(token='vk1.a.TZz6TMz6LD1BS04uaWaRJqgtrRa2ZkcvRwFrKfnthjK8P2PUnmHlID7HvIpXo0jmuqgFGzG3k59zS-8bLQ15z71ksk1ZXIhKNYkZNLQP-cghdXD0DQni025BufAHJgItODMGnyPf6XkcmwkUjKActFekQEr8w331stppSjUzqcDgE7yjazih7kFZqtE9RFS1NMfRy2pFmFTg32NF-_NrXA')
vk = vk_session.get_api()

# ID пользователя, которому отправляешь видео
user_id = 570608908

video_path = 'path/to/your_video.mp4'

# upload_url_response = vk.video.save(
#     name='Видео от бота',
#     description='Видео, отправленное через бота',
#     is_private=1
# )

# upload_url = upload_url_response['upload_url']
# video_owner_id = upload_url_response['owner_id']
# video_id = upload_url_response['video_id']

# with open(video_path, 'rb') as video_file:
#     response = requests.post(upload_url, data={'link': "https://ideasformuseums.com/botimages/video/course-1_lecture-1.mp4"})


vk.messages.send(
    user_id=user_id,
    attachment=f'video-232058422_456239018',
    random_id=0
)
