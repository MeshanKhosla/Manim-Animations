from manimlib.imports import *

class Grid(VGroup):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))

class ScreenGrid(VGroup):
    CONFIG = {
        "rows": 8,
        "columns": 14,
        "height": FRAME_Y_RADIUS * 2,
        "width": 14,
        "grid_stroke": 0.5,
        "grid_color": WHITE,
        "axis_color": RED,
        "axis_stroke": 2,
        "labels_scale": 0.25,
        "labels_buff": 0,
        "number_decimals": 2
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rows = self.rows
        columns = self.columns
        grid = Grid(width=self.width, height=self.height, rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        axes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        axes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisions_x = self.width / columns
        divisions_y = self.height / rows

        directions_buff_x = [UP, DOWN]
        directions_buff_y = [RIGHT, LEFT]
        dd_buff = [directions_buff_x, directions_buff_y]
        vectors_init_x = [vector_ii, vector_si]
        vectors_init_y = [vector_si, vector_sd]
        vectors_init = [vectors_init_x, vectors_init_y]
        divisions = [divisions_x, divisions_y]
        orientations = [RIGHT, DOWN]
        labels = VGroup()
        set_changes = zip([columns, rows], divisions, orientations, [0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = Text(f"{coord_point}",font="Arial",stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff, buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)

class Title(VGroup):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        rotate_left_txt = TextMobject(text)
        rotate_left_txt.to_corner(UL)
        self.add(rotate_left_txt)
        
class LLNode(VGroup):
    def __init__(self, value, pos, is_end, **kwargs):
        super().__init__(**kwargs)

        DIMENSIONS = 1.25
        ARROW_DISTANCE = DIMENSIONS / 3
        self.value_box = Square(side_length=DIMENSIONS)
        self.pointer_box = Square(side_length=DIMENSIONS)

        self.pointer_box.move_to(np.array([DIMENSIONS, 0, 1]))
        node = VGroup(self.value_box, self.pointer_box)
        node.move_to(np.array([pos[0], pos[1], 1]))

        text = TextMobject(value)
        text.move_to(self.value_box.get_center())

        self.arrow = CurvedArrow(
                    start_point=self.pointer_box.get_center(), 
                    end_point=(node.get_edge_center(RIGHT)[0] + ARROW_DISTANCE,
                               node.get_edge_center(RIGHT)[1],
                               node.get_edge_center(RIGHT)[2]),
                    angle=0 # This changes when animation begins
                )
        if is_end:
            self.arrow = Line(self.pointer_box.get_start(), 
                         self.pointer_box.get_corner(DR))
        # Only adds the single node if it is a null node
        if kwargs.get("null_node", False):
            self.add(self.pointer_box, self.arrow)
            return
            
        self.add(node, text, self.arrow)

class ReverseLL(Scene):
    def setup(self):
        grid = ScreenGrid()
        # self.add(grid)

    def construct(self):
        # Adds title text
        self.wait(.3)
        title = Title("ReverseSLL(L)")
        self.play(FadeInFrom(title, UP))
        self.wait(.5)

        starting_null_node = LLNode("", [-6.7, 0], True, null_node=True)
        node_1 = LLNode("1", [-3.7, 0], False)
        node_2 = LLNode("2", [-0.7, 0], False)
        node_3 = LLNode("3", [2.3, 0], False)
        node_4 = LLNode("4", [5.3, 0], True)

        self.play(
            ShowCreation(starting_null_node),
            ShowCreation(node_1),
            ShowCreation(node_2),
            ShowCreation(node_3),
            ShowCreation(node_4)
        )
        

        # Adds starting arrows
        next_arrow = self.make_arrow([-6, -2, 0], [-6, -.625, 0], BLUE)
        next_txt = TextMobject("Next", color=BLUE)
        self.connect_arrow_to_txt(next_arrow, next_txt, 0.3)

        prev_arrow = self.make_arrow([-6, 2, 0], [-6, 0.625, 0], PINK)
        prev_txt = TextMobject("Prev", color=PINK)
        self.connect_arrow_to_txt(prev_arrow, prev_txt, -1.7)

        head_arrow = self.make_arrow([-4.3, 2, 0], [-4.3, 0.625, 0], ORANGE)
        head_txt = TextMobject("Head", color=ORANGE)
        self.connect_arrow_to_txt(head_arrow, head_txt, -1.7)

        curr_arrow = self.make_arrow([-3, 2, 0], [-4.3, 0.625, 0], RED)
        curr_txt = TextMobject("Curr", color=RED)
        self.connect_arrow_to_txt(curr_arrow, curr_txt, -1.7, -.75)
        self.wait(0.5)

        self.play(
            ShowCreation(next_arrow), 
            ShowCreation(next_txt), 
            ShowCreation(prev_arrow), 
            ShowCreation(prev_txt),
            ShowCreation(head_txt), 
            ShowCreation(head_arrow), 
            ShowCreation(curr_arrow), 
            ShowCreation(curr_txt)
        )

        self.wait(1)

        """
        Below this comment is the recursive Linked List reversal algorithm:
            1. Next gets progressed
            2. Pointer gets swapped
            3. Prev gets progressed
            4. Curr gets progressed
        """
        self.progress_next_path(next_arrow, 4.7)
        self.wait(.5)
        
        self.swap_arrow(node_1, starting_null_node)
        self.wait(.5)

        prev_arrow_new = self.make_arrow([-5.5, 2, 0], [-4.3, 0.625, 0], PINK)
        prev_txt_new = TextMobject("Prev", color=PINK)
        prev_txt_new.move_to((-5.6, 2.35, 0))
        self.play(
            Transform(prev_arrow, prev_arrow_new),
            FadeOut(prev_txt),
            FadeIn(prev_txt_new)
        )
        self.wait(.5)

        curr_arrow_new = self.make_arrow([-1.3, 2, 0], [-1.3, 0.625, 0], RED)
        curr_txt_new = TextMobject("Curr", color=RED)
        curr_txt_new.move_to((-1.3, 2.35, 0))
        self.play(
            Transform(curr_arrow, curr_arrow_new),
            FadeOut(curr_txt),
            FadeIn(curr_txt_new)
        )
        self.wait(.5)

        self.progress_next_path(next_arrow, 3)
        self.wait(.5)

        self.swap_arrow(node_2, node_1)
        self.wait(.5)

        prev_arrow_new = self.make_arrow([-2.3, 2, 0], [-1.3, 0.625, 0], PINK)
        prev_txt_1 = TextMobject("Prev", color=PINK)
        prev_txt_1.move_to((-2.5, 2.35, 0))
        self.play(
            Transform(prev_arrow, prev_arrow_new),
            FadeOut(prev_txt_new),
            FadeIn(prev_txt_1)
        )
        self.wait(.5)

        curr_arrow_new = self.make_arrow([1.65, 2, 0], [1.65, 0.625, 0], RED)
        curr_txt_1 = TextMobject("Curr", color=RED)
        curr_txt_1.move_to((1.65, 2.35, 0))
        self.play(
            Transform(curr_arrow, curr_arrow_new),
            FadeOut(curr_txt_new),
            FadeIn(curr_txt_1)
        )
        self.wait(.5)

        self.progress_next_path(next_arrow, 3)
        self.wait(.5)

        self.swap_arrow(node_3, node_2)
        self.wait(.5)

        prev_arrow_new = self.make_arrow([0.5, 2, 0], [1.65, 0.625, 0], PINK)
        prev_txt_2 = TextMobject("Prev", color=PINK)
        prev_txt_2.move_to((0.5, 2.35, 0))
        self.play(
            Transform(prev_arrow, prev_arrow_new),
            FadeOut(prev_txt_1),
            FadeIn(prev_txt_2)
        )
        self.wait(.5)

        curr_arrow_new = self.make_arrow([5.65, 2, 0], [4.65, 0.625, 0], RED)
        curr_txt_2 = TextMobject("Curr", color=RED)
        curr_txt_2.move_to((5.85, 2.35, 0))
        self.play(
            Transform(curr_arrow, curr_arrow_new),
            FadeOut(curr_txt_1),
            FadeIn(curr_txt_2)
        )
        self.wait(.5)

        self.progress_next_path(next_arrow, 3)
        self.wait(.5)

        self.swap_arrow(node_4, node_3)
        self.wait(.5)

        prev_arrow_new = self.make_arrow([4.65, 2, 0], [4.65, 0.625, 0], PINK)
        prev_txt_3 = TextMobject("Prev", color=PINK)
        prev_txt_3.move_to((4.65, 2.35, 0))
        self.play(
            Transform(prev_arrow, prev_arrow_new),
            FadeOut(prev_txt_2),
            FadeIn(prev_txt_3)
        )
        self.wait(.5)

        # Yeets off screen
        curr_arrow_new = self.make_arrow([7.5, 2, 0], [7.5, 0.625, 0], RED)
        self.play(
            Transform(curr_arrow, curr_arrow_new),
            FadeOut(curr_txt_2),
        )
        self.wait(.5)

        head_arrow_new = self.make_arrow([4.65, 2, 0], [4.65, 0.625, 0], ORANGE)
        self.play(
            Transform(head_arrow, head_arrow_new),
            FadeOut(prev_txt_3),
            FadeOut(prev_arrow)
        )
        self.wait(3)



    def progress_next_path(self, next_arrow, shift):
        next_path = Line(
            start=np.array([
                next_arrow.get_top()[0],
                next_arrow.get_top()[1] - (next_arrow.get_length() / 2),
                next_arrow.get_top()[1],]),
            end=np.array([
                next_arrow.get_top()[0] + shift,
                next_arrow.get_top()[1] - (next_arrow.get_length() / 2),
                next_arrow.get_top()[2],])
        )
        next_path.set_opacity(0)
        self.add(next_path)
        self.play(
            MoveAlongPath(next_arrow, next_path, run_time=1)
        )

    def make_arrow(self, start, end, color):
        new_arrow = CurvedArrow(
            start_point=np.array(start),
            end_point=np.array(end),
            angle=0,
            color=color,
        )
        return new_arrow

    def swap_arrow(self, node, target_node):
        new_arrow = CurvedArrow(
            start_point=np.array([
                node.pointer_box.get_bottom()[0],
                node.pointer_box.get_bottom()[1] + .625,
                node.pointer_box.get_bottom()[2],
            ]),
            end_point=target_node.get_bottom(),
            angle=-PI/2
        )
        self.play(
            Transform(node.arrow, new_arrow, run_time=1)
        )

        
    def connect_arrow_to_txt(self, arrow, txt, buffer, horizontal_buffer=0):
        # Makes sure text stays centered on node
        txt.add_updater(lambda m: m.move_to(np.array([
            arrow.get_bottom()[0] - horizontal_buffer,
            arrow.get_bottom()[1] - buffer,
            arrow.get_bottom()[2]
        ])))
    
    def connect_node_to_arrow(self, node, arrow, buffer):
        # Makes sure arrow stays centered on node -- not needed for this animation
        # but might be useful in the future
        arrow.add_updater(lambda m: m.move_to(np.array([
            node.get_bottom()[0],
            node.get_bottom()[1] - buffer,
            node.get_bottom()[2]
        ])))