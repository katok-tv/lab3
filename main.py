from struct import pack
import numpy as np


def create_dots():
    t = np.linspace(0, 2 * np.pi, 500)
    np_x = (6 * np.cos(t)) - (4 * (np.cos(t)) ** 3)
    np_y = 4 * ((np.sin(t)) ** 3)

    x = [round(i, 2) for i in np_x]
    y = [round(i, 2) for i in np_y]

    min_x, min_y = min(x), min(y)

    dots = [(x[i], y[i]) for i in range(len(x))]

    dots.reverse()
    return min_x, min_y, dots


def create_bmp_header(width, height):
    file_type = 19778     # 'BM'
    reserved_1 = 0
    reserved_2 = 0
    pixel_data_offset = 62      # 54 + 8
    file_size = pixel_data_offset + 1 * width * height
    return pack("<hi2hi", file_type, file_size, reserved_1, reserved_2, pixel_data_offset)


def create_info_header(width, height):
    header_size = 40
    planes = 1
    bits_per_pixel = 8
    compression = 0
    img_size = 0
    x_px_per_meter = 0
    y_px_per_meter = 0
    total_colors = 2
    important_colors = 0
    return pack(
        "<3i2h6i",
        header_size, width, height, planes, bits_per_pixel,
        compression, img_size, x_px_per_meter, y_px_per_meter,
        total_colors, important_colors
    )


def create_color_table():
    color_1 = (0, 0, 0, 0)
    color_2 = (255, 255, 255, 0)
    return pack("<8B", *color_1, *color_2)  # * - распаковка кортежа


def write_file(step, width, height, filename):
    with open("{}.bmp".format(filename), "wb") as f:
        f.write(create_bmp_header(width, height))
        f.write(create_info_header(width, height))
        f.write(create_color_table())
        min_x, min_y, dots = create_dots()

        y_pix = min_y
        for i in range(height):
            x_pix = min_x
            for j in range(width):
                if (x_pix, y_pix) in dots:
                    f.write(pack("<B", 0))
                else:
                    f.write(pack("<B", 1))
                x_pix = round(x_pix + step, 2)
            y_pix = round(y_pix + step, 2)


if __name__ == "__main__":
    write_file(0.01, 800, 1000, "result")
