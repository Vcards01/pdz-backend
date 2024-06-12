import os
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from src.entities.video import VideoRequest
from src.entities.user import UserComplete
from src.use_cases.user import UserService
from src.auth import oauth_2_scheme
from pathlib import Path
import yt_dlp
import subprocess

from src.use_cases.discord_user import DiscordUserService
router = APIRouter()


def remove_file(file_path: str):
    os.remove(file_path)

def merge_audio_video(video_path: Path, audio_path: Path, output_path: Path):
    subprocess.run(['ffmpeg', '-i', str(video_path), '-i', str(audio_path), '-c', 'copy', str(output_path)])

@router.post("/download_video/")
async def download_video(request: VideoRequest, background_tasks: BackgroundTasks, token: str = Depends(oauth_2_scheme), user_service: UserService = Depends(UserService), discord_user_service: DiscordUserService = Depends(DiscordUserService)):
    try:
        await user_service.get_user_by_token(token=token)
    except Exception:
        if not discord_user_service.check_discord_token(token=token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possivel validar suas credenciais",
                headers={"WWW-Authenticate": "Bearer"},
            )

    temp_dir = Path('temp_videos')
    temp_dir.mkdir(exist_ok=True)
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': str(temp_dir / 'video.%(ext)s'),
        'noplaylist': True,
        'postprocessors': [],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(request.url, download=True)
            #video_title = info_dict.get('title', "video").replace(" ","_")
            video_ext = info_dict.get('ext', 'mp4')

            # Obtenha o caminho do arquivo de vídeo baixado
            video_path = temp_dir / f"video.{video_ext}"

            # Verifique se há um arquivo de áudio separado
            audio_formats = [f for f in info_dict.get('formats', []) if f.get('acodec') != 'none']
            if len(audio_formats) == 1:
                audio_url = audio_formats[0].get('url')
                audio_ext = audio_formats[0].get('ext', 'mp3')
                audio_path = temp_dir / f"video_audio.{audio_ext}"
                
                # Baixe o áudio separadamente
                subprocess.run(['curl', '-L', audio_url, '--output', str(audio_path)])

                # Mesclar áudio e vídeo
                output_filename = f"video_merged.{video_ext}"
                output_path = temp_dir / output_filename
                background_tasks.add_task(merge_audio_video, video_path, audio_path, output_path)

                return StreamingResponse(
                    output_path.open('rb'),
                    media_type=f'video/{video_ext}',
                    headers={
                        "Content-Disposition": f"attachment; filename={output_filename}"
                    }
                )
            else:
                # Não há áudio separado disponível, retornar o vídeo como está
                background_tasks.add_task(remove_file, str(video_path))

                return StreamingResponse(
                    video_path.open('rb'),
                    media_type=f'video/{video_ext}',
                    headers={
                        "Content-Disposition": f"attachment; filename=video.{video_ext}"
                    }
                )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))