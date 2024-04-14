import pygame
import random
import math

pygame.init()

class Visualizer:
    black = 0, 0, 0
    white = 255, 255, 255
    green = 0, 255, 0
    red = 255, 0, 0
    blue = 0, 0, 255
    grey = 128, 128, 128

    # Gradients for the list bars
    light_blue = 167, 199, 231  # Lightest
    aqua = 0, 255, 255  # Light
    neon_blue = 31, 81, 255  # Little Dark

    bg_color = black
    side_pad = 100
    top_pad = 150

    font = pygame.font.SysFont('Kodchasan Bold', 25)
    largefont = pygame.font.SysFont('Kodchasan Bold', 35)

    gradients = [light_blue, aqua, neon_blue]

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.setlist(lst)

    def setlist(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)
        self.block_width = round((self.width - self.side_pad) / len(lst))
        self.block_height = math.floor((self.height - self.top_pad) / (self.max_val - self.min_val))
        self.start_x = self.side_pad // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.bg_color)


    title = draw_info.largefont.render(f"Selected Sort: {algo_name} - {'Ascending' if ascending else 'Descending'}", 1,
                                        draw_info.green)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.font.render("R- Reset | Enter - Start Sorting | A - Ascending | D - Descending", 1,
                                        draw_info.white)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 35))

    controls = draw_info.font.render("B - Bubble Sort | S - Selection Sort | I - Insertion Sort", 1, draw_info.white)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 55))

    controls = draw_info.font.render("M - Merge Sort | Q - Quick Sort", 1, draw_info.white)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 75))

    controls = draw_info.font.render("T - Shell Sort", 1, draw_info.white)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 95))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.side_pad // 2, 
                        draw_info.top_pad, 
                        draw_info.width - draw_info.side_pad,
                        draw_info.height - draw_info.top_pad)
        pygame.draw.rect(draw_info.window, draw_info.bg_color, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.gradients[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_list(n, min_val, max_val):
    lst = []
    for i in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 150
    min_val = 0
    max_val = 100

    lst = generate_list(n, min_val, max_val)
    draw_info = Visualizer(1280, 720, lst)

    ascending = False
    descending = False

    sorting = False
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False

                for i in range(len(draw_info.lst)):
                    draw_list(draw_info, {i: draw_info.green}, True)
                    pygame.time.delay(10)
                    pygame.display.update()
        else:
            draw(draw_info, sorting_algorithm_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_list(n, min_val, max_val)
                draw_info.setlist(lst)
                sorting = False

            elif event.key == pygame.K_RETURN and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
                descending = False

            elif event.key == pygame.K_d and not sorting:
                ascending = False
                descending = True

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm_name = "Bubble Sort"
                sorting_algorithm = bubble_sort

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm_name = "Insertion Sort"
                sorting_algorithm = insertion_sort

            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm_name = "Selection Sort"
                sorting_algorithm = selection_sort

            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm_name = "Merge Sort"
                sorting_algorithm = merge_sort
                merge_sort_generator = merge_sort(draw_info, ascending)

                if sorting:
                    try:
                        next(merge_sort_generator)  # Execute the first step of merge sort
                    except StopIteration:
                        sorting = False
                else:
                    draw(draw_info, sorting_algorithm_name, ascending)

            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm_name = "Quick Sort"
                sorting_algorithm = quick_sort

            elif event.key == pygame.K_t and not sorting:
                sorting_algorithm_name = "Shell Sort"
                sorting_algorithm = shell_sort


    pygame.quit()

#Bubble Sort
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]  # Swapping
                draw_list(draw_info, {j: draw_info.green, j + 1: draw_info.red}, True)
                yield True
    return True

#Selection Sort
def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst)):
        min_idx = i
        for j in range(i + 1, len(lst)):
            if (lst[min_idx] > lst[j] and ascending) or (lst[min_idx] < lst[j] and not ascending):
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i: draw_info.green, min_idx: draw_info.red}, True)  # Update visualization after swapping
        yield True
    return True

#Insertion Sort
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]
        j = i - 1
        while j >= 0 and ((lst[j] > current and ascending) or (lst[j] < current and not ascending)):
            lst[j + 1] = lst[j]
            draw_list(draw_info, {j: draw_info.green, j + 1: draw_info.red}, True)  # Update visualization after swapping
            yield True
            j -= 1
        lst[j + 1] = current
    return True

#Merge Sort
def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst
    yield from merge_sort_recursive(draw_info, lst, 0, len(lst) - 1, ascending, {})

    return True

def merge_sort_recursive(draw_info, lst, left, right, ascending=True, color_positions=None):
    if color_positions is None:
        color_positions = {}  # Create a new dictionary if None

    if left < right:
        mid = (left + right) // 2
        yield from merge_sort_recursive(draw_info, lst, left, mid, ascending, color_positions.copy())
        yield from merge_sort_recursive(draw_info, lst, mid + 1, right, ascending, color_positions.copy())
        yield from merge(draw_info, lst, left, mid, right, ascending, color_positions)

    yield True

def merge(draw_info, lst, left, mid, right, ascending=True, color_positions={}):
    left_half = lst[left:mid + 1]
    right_half = lst[mid + 1:right + 1]
    i = j = 0
    k = left

    while i < len(left_half) and j < len(right_half):
        if (left_half[i] <= right_half[j] and ascending) or (left_half[i] > right_half[j] and not ascending):
            lst[k] = left_half[i]
            i += 1
        else:
            lst[k] = right_half[j]
            j += 1
        k += 1

    while i < len(left_half):
        lst[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        lst[k] = right_half[j]
        j += 1
        k += 1

    draw_list(draw_info, color_positions, True)

    yield True

#Quick Sort
def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst
    yield from quick_sort_recursive(draw_info, lst, 0, len(lst) - 1, ascending, {})

    return True

def quick_sort_recursive(draw_info, lst, low, high, ascending=True, color_positions={}):
    if low < high:
        pi = yield from partition(draw_info, lst, low, high, ascending, color_positions)
        yield from quick_sort_recursive(draw_info, lst, low, pi - 1, ascending, color_positions)
        yield from quick_sort_recursive(draw_info, lst, pi + 1, high, ascending, color_positions)

    yield True

def partition(draw_info, lst, low, high, ascending=True, color_positions={}):
    pivot = lst[high]
    i = low - 1
    for j in range(low, high):
        if (lst[j] <= pivot and ascending) or (lst[j] > pivot and not ascending):
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            draw_list(draw_info, {i: draw_info.green, j: draw_info.red}, True)
    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    draw_list(draw_info, {i + 1: draw_info.green, high: draw_info.red}, True)
    yield True
    return i + 1

def shell_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = lst[i]
            j = i
            while j >= gap and ((lst[j - gap] > temp and ascending) or (lst[j - gap] < temp and not ascending)):
                lst[j] = lst[j - gap]
                j -= gap
            lst[j] = temp
            draw_list(draw_info, {i: draw_info.green}, True)  # Update visualization after each step
            yield True
        gap //= 2
    return True

if __name__ == "__main__":
    main()
