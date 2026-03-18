import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np

# ============================================================
# MAZE 15x15 (0=dinding, 1=jalan)
# ============================================================
MAZE = [
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,0,1,0,1,0,0,0,1,0,1,0,1],
    [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
    [0,0,0,0,0,0,1,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,1,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,1,1,0,1,1,1,1,1,0,1,1,1,0,1],
    [0,0,1,0,1,0,0,0,1,0,1,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,0,1,1,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
]
N = len(MAZE)
START = (0, 0)
END = (N-1, N-1)

# ============================================================
# COLOR SCHEME
# ============================================================
COLOR_MAP = {
    'wall':        [0.10, 0.10, 0.18],  # gelap
    'unvisited':   [0.91, 0.91, 0.91],  # abu terang
    'visited':     [0.66, 0.84, 0.89],  # biru muda
    'current':     [0.97, 0.72, 0.19],  # kuning (posisi tikus)
    'backtracked': [1.00, 0.42, 0.42],  # merah (dead end)
    'solution':    [0.13, 0.75, 0.42],  # hijau (solusi)
}

# ============================================================
# BACKTRACKING + FRAME CAPTURE
# ============================================================
frames = []
path_stack = []
solutions = []
visited = [[False]*N for _ in range(N)]
grid_state = [['wall' if MAZE[r][c]==0 else 'unvisited'
                for c in range(N)] for r in range(N)]

def capture_frame(r, c, action, depth):
    frames.append({
        'grid': [row[:] for row in grid_state],
        'pos': (r, c), 'action': action, 'depth': depth,
        'path_len': len(path_stack),
    })

def backtrack(r, c, depth=0):
    if r < 0 or r >= N or c < 0 or c >= N: return False
    if MAZE[r][c] == 0 or visited[r][c]: return False
    
    visited[r][c] = True
    path_stack.append((r, c))
    grid_state[r][c] = 'current'
    capture_frame(r, c, 'visit', depth)

    if (r, c) == END:
        solutions.append(path_stack[:])
        for pr, pc in path_stack:
            grid_state[pr][pc] = 'solution'
        capture_frame(r, c, 'done', depth)
        path_stack.pop()
        visited[r][c] = False
        return True

    grid_state[r][c] = 'visited'
    for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
        if backtrack(r+dr, c+dc, depth+1): return True

    grid_state[r][c] = 'backtracked'
    path_stack.pop()
    visited[r][c] = False
    capture_frame(r, c, 'backtrack', depth)
    return False

backtrack(0, 0)

# ============================================================
# ANIMATED VISUALIZATION
# ============================================================
fig, (ax_maze, ax_info) = plt.subplots(1, 2, figsize=(14, 8),
    facecolor='#0f0f1a', gridspec_kw={'width_ratios': [2, 1]})

def grid_to_rgb(grid):
    rgb = np.zeros((N, N, 3))
    for r in range(N):
        for c in range(N):
            rgb[r][c] = COLOR_MAP.get(grid[r][c], COLOR_MAP['unvisited'])
    return rgb

img = ax_maze.imshow(grid_to_rgb(frames[0]['grid']), interpolation='nearest')
rat_dot, = ax_maze.plot(0, 0, 'o', markersize=14, color='#f7b731',
                         markeredgecolor='white', markeredgewidth=1.5, zorder=8)
ax_maze.set_xticks([]); ax_maze.set_yticks([])
ax_maze.spines[:].set_color('#f7b731')
ax_maze.text(0, 0, 'S', ha='center', va='center', color='white', fontweight='bold', fontsize=9, zorder=9)
ax_maze.text(N-1, N-1, 'E', ha='center', va='center', color='white', fontweight='bold', fontsize=9, zorder=9)

ax_info.set_facecolor('#13131f'); ax_info.axis('off')
ax_info.set_xlim(0,10); ax_info.set_ylim(0,10)
lbl_frame  = ax_info.text(0.5, 8.5, '', fontsize=11, color='white')
lbl_action = ax_info.text(0.5, 7.5, '', fontsize=11, color='#a8d5e2')
lbl_depth  = ax_info.text(0.5, 6.5, '', fontsize=11, color='white')
lbl_path   = ax_info.text(0.5, 5.5, '', fontsize=11, color='#a8d5e2')

def update(fi):
    frame = frames[fi]
    img.set_data(grid_to_rgb(frame['grid']))
    r, c = frame['pos']
    rat_dot.set_data([c], [r])
    lbl_frame.set_text(f"Frame  : {fi+1}/{len(frames)}")
    lbl_action.set_text(f"Aksi   : {frame['action'].upper()}")
    lbl_depth.set_text(f"Depth  : {frame['depth']}")
    lbl_path.set_text(f"Panjang: {frame['path_len']} langkah")
    return img, rat_dot, lbl_frame, lbl_action, lbl_depth, lbl_path

ani = animation.FuncAnimation(fig, update, frames=len(frames),
                               interval=250, blit=True, repeat=True)
ani.save('rat_in_maze_animation.gif', writer=animation.PillowWriter(fps=4), dpi=90)
plt.show()
