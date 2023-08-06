import os

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from processing.batch.reconstruct import EndoStack
from processing.files.files import EndoFiles


def get_ffmpeg_path() -> str:
    thispath = os.path.dirname(__file__)
    relpath = os.path.relpath(thispath)
    libspath = os.path.join(relpath, "libs", "ffmpeg.exe")
    return os.path.join(libspath, "ffmpeg.exe")


class VideoExport:
    _default_video_name = 'stacked_recon'
    _default_video_ext = '.avi'
    _defaut_video_path = 'C:\\Temp'
    _default_figure_size = (9, 8)
    _default_ffmpeg_path = get_ffmpeg_path()

    def __init__(self, stack: EndoStack, savedir: str = '', savename: str = '', video_fps: int = 10,
                 colormap: str = 'gray'):
        self.timestamps = stack.timestamps
        self.image_size = stack.image_size
        self.channels = stack.channels
        self.fill_unsampled = stack.fill_unsampled
        self.video_fps = video_fps
        self.savedir = VideoExport._defaut_video_path if not savedir else savedir
        self.savename = savename
        self.colormap = colormap

    def export(self, stack: EndoStack, channel: str = 'PMT1'):
        fig, ax, imh, title = self._init_figure()
        channel_idx = self.channels.index(channel)
        stack_size = stack.stack_shape

        def update_plot(frame):
            img = stack.stack[frame, channel_idx, :, :]
            imh.set_data(img)
            imh.set_clim(np.min(img), np.max(img))
            plt.title(self.timestamps[frame])

        ani = animation.FuncAnimation(
            fig,
            func=update_plot,
            interval=100,
            frames=stack_size[0] - 1,
        )

        plt.draw()

        self.savename = self._construct_savename()
        ffwriter = animation.FFMpegWriter(fps=self.video_fps, extra_args=['-vcodec', 'libx264'])
        ani.save(filename=os.path.join(self.savedir, self.savename), writer=ffwriter)

    @staticmethod
    def _init_matplotlib() -> None:
        plt.rcParams['text.color'] = 'black'
        plt.rcParams['animation.ffmpeg_path'] = VideoExport._default_ffmpeg_path

    def _init_figure(self) -> tuple[plt.Figure, plt.Axes, matplotlib.image.AxesImage, str]:
        self._init_matplotlib()
        fig = plt.figure(figsize=VideoExport._default_figure_size, facecolor='black')
        fig.patch.set_visible(False)
        ax = plt.gca()
        ax.axis('off')
        pl = ax.imshow(np.zeros((self.image_size, self.image_size)), cmap=self.colormap, interpolation='none')
        title = plt.title('')
        return fig, ax, pl, title

    def _construct_savename(self):
        if self.savename:
            return self.savename + VideoExport._default_video_ext
        else:
            imsize = f"_imgsize={self.image_size}"
            tstamps = f"_start={self.timestamps[0]}_stop={self.timestamps[-1]}"
            filled = f"_filled={self.fill_unsampled}"
            suffix = imsize + tstamps + filled
            return VideoExport._default_video_name + suffix + VideoExport._default_video_ext


if __name__ == '__main__':
    fs = EndoFiles(
        path='C:/Users/jerem/Downloads/tufts_20221114/raw_G202207-06_obj=2100um4fps/'
    )
    fs.filter_days(days=['20221114'])
    fs.filter_times(between=['231300', '231320'])
    print(fs)

    stack = EndoStack(files=fs, channels=['PMT1', 'PMT2'], image_size=250, fill_unsampled=False)
    stack.build(display_progress=True)
    stack.save()

    vid = VideoExport(stack=stack)
    vid.export(stack=stack, channel='PMT1')
