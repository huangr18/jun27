import moviepy.editor as moviepy


def convert(videoname):
    clip = moviepy.VideoFileClip('result/%s'%videoname)
    clip.write_videofile('.mp4')
    return videoname
