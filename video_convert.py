import moviepy.editor as moviepy


def convert(videoname):
    clip = moviepy.VideoFileClip('static/result/%s'%videoname)
    # fps = clip.fps
    clip.write_videofile('static/result/con%s'%videoname, fps=30, threads=1, codec="libx264")
    return videoname

# convert('result_jimhv7.mp4')
convert('result_jul5.mp4')