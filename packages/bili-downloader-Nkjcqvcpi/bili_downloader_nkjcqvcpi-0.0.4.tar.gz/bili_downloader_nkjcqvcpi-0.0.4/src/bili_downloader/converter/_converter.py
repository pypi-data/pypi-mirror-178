import subprocess


def merge(output, video=None, audio=None):
    cmd = ['ffmpeg']
    if video:
        cmd.extend(['-i', video])
    if audio:
        cmd.extend(['-i', audio])
    cmd.extend(['-c', 'copy', '-y', output])
    subprocess.run(cmd)
    return output
