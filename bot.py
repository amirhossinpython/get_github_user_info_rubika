from rubpy import Client, filters, utils  
from rubpy.types import Updates  
import requests  
import os  

bot = Client(name='get_github_user_info')  

async def is_valid_github_username(username):  
    url = f"https://api.github.com/users/{username}"  
    response = requests.get(url)  
    return response.status_code == 200  

def get_github_user_info(username):  
    url = f"https://api.github.com/users/{username}"  
    response = requests.get(url)  
    return response.json() if response.status_code == 200 else None  

async def download_profile_image(url, username):  
    image_path = f"{username}_profile.jpg"  
    response = requests.get(url)  
    
    if response.status_code == 200:  
        with open(image_path, 'wb') as f:  
            f.write(response.content)  
        return image_path  
    return None  

async def display_user_info(update, user_info):  
    if user_info:  
        response_text = (  
            "🧑‍💻 جزئیات کاربر GitHub:\n"  
            f"📛 نام کاربری: {user_info['login']}\n"  
            f"🔑 شناسه کاربر: {user_info['id']}\n"  
            f"🌐 آدرس پروفایل: {user_info['html_url']}\n"  
            f"👥 تعداد دنبال‌کنندگان: {user_info['followers']}\n"  
            f"👤 تعداد دنبال‌شوندگان: {user_info['following']}\n"  
            f"📂 تعداد ریپوزیتوری‌های عمومی: {user_info['public_repos']}\n"  
            f"📅 تاریخ عضویت: {user_info['created_at']}\n"  
            f"✍️ بیوگرافی: {user_info['bio'] if user_info['bio'] else 'ندارد'}"  
        )  
        
        if user_info.get('avatar_url'):  
            image_path = await download_profile_image(user_info['avatar_url'], user_info['login'])  
            
            if image_path:  
                await update.reply_photo(image_path, caption=response_text)  
                os.remove(image_path)  
            else:  
                await update.reply(response_text)  
        else:  
            await update.reply(response_text) 
    else:  
        await update.reply("❌ نام کاربری GitHub معتبر نیست!") 
@bot.on_message_updates(filters.is_private)  
async def updates(update: Updates):  
    username = update.text.strip()  
    
    if not await is_valid_github_username(username):  
        await update.reply("❌ لطفا شناسه کاربری خود را در صفحه GitHub بدهید تا بتونم برات فعالیت هاشو تحلیل کنم و بفرستم واست.")  
        return  
    
    user_info = get_github_user_info(username)  
    await display_user_info(update, user_info)  

    stats_url = f"https://github-readme-stats.vercel.app/api?username={username}&show_icons=true&count_private=true&theme=radical"  
    languages_url = f"https://github-readme-stats.vercel.app/api/top-langs/?username={username}&layout=compact&theme=radical"  
    animation_url = "https://raw.githubusercontent.com/imrrobat/imrrobat/d1b244e170d2b75fdda3efd499eaaf163f7a617c/images/github-contribution-grid-snake.svg"  

    await update.reply_document(stats_url, f"📊 آمار GitHub:\n{stats_url}")  
    await update.reply_document(languages_url, f"🌐 زبان‌های برتر:\n{languages_url}")  
    await update.reply_document(animation_url, f"🐍 انیمیشن مار:\n{animation_url}")  

bot.run()   
