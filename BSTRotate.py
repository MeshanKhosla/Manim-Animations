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


class BSTRotateAnimation(Scene):
    CONFIG = {
        # Node 3 curve up
        "x_coords_n3_1":[2.5, 2.4, 2,   1.5, 1.25, 1],
        "y_coords_n3_1":[0,   1,   1.75, 2,   2,   2],

        # Node 1 moving to the left
        "x_coords_n1_1": [0,  -0.5,   -1,   -1.5],
        "y_coords_n1_1": [2,   2,     1.75,  1],

        # Node 3 moving left to root position
        "x_coords_n3_2": [1, 0],
        "y_coords_n3_2": [2, 2]
    }
    def setup(self):
        grid = ScreenGrid()
        # self.add(grid)
        self.path_n3_1 = list(zip(self.x_coords_n3_1,self.y_coords_n3_1))
        self.path_n1_1 = list(zip(self.x_coords_n1_1,self.y_coords_n1_1))
        self.path_n3_2 = list(zip(self.x_coords_n3_2,self.y_coords_n3_2))

    def construct(self):
        # Adds title text
        self.wait(.3)
        rotate_left_txt = TextMobject("rotateLeft(G)")
        rotate_left_txt.to_corner(UL)
        self.play(FadeInFrom(rotate_left_txt, UP))
        self.wait(.5)

        # Node 1 
        node_1 = self.make_node()
        node_1_txt = self.make_node_text(BLUE, "G")
        self.connect_node(node_1, node_1_txt)

        self.play(ShowCreation(node_1, run_time=1))
        self.play(FadeIn(node_1_txt, run_time=.2))
        self.play(node_1.move_to, UP * 2)

        # Node 2
        node_2 = self.make_node()
        node_2_txt = self.make_node_text(BLUE, "C")
        self.connect_node(node_2, node_2_txt)

        # Node 3
        node_3 = self.make_node()
        node_3_txt = self.make_node_text(BLUE, "P")
        self.connect_node(node_3, node_3_txt)

        self.play(DrawBorderThenFill(node_3, run_time=1), DrawBorderThenFill(node_2, run_time=1))
        self.play(
            node_3.move_to, UP * 0 + RIGHT * 2.5, 
            node_2.move_to, UP * 0 + LEFT * 2.5
        )
        self.play(
            FadeIn(node_2_txt, run_time=.2), 
            FadeIn(node_3_txt, run_time=.2)
        )

        # Node 4
        node_4 = self.make_node()
        node_4_txt = self.make_node_text(BLUE, "A")
        self.connect_node(node_4, node_4_txt)

        # Node 5
        node_5 = self.make_node()
        node_5_txt = self.make_node_text(BLUE, "K")
        self.connect_node(node_5, node_5_txt)

        # Node 6
        node_6 = self.make_node()
        node_6_txt = self.make_node_text(BLUE, "R")
        self.connect_node(node_6, node_6_txt)


        self.play(
            DrawBorderThenFill(node_4, run_time=1), 
            DrawBorderThenFill(node_5, run_time=1), 
            DrawBorderThenFill(node_6, run_time=1),
        )

        self.play(
            node_4.move_to, DOWN * 2 + LEFT * 4,
            node_5.move_to, DOWN * 2 + RIGHT,
            node_6.move_to, DOWN * 2 + RIGHT * 4,
        )
        self.play(
            FadeIn(node_4_txt, run_time=.2), 
            FadeIn(node_5_txt, run_time=.2),
            FadeIn(node_6_txt, run_time=.2)
        )


        # Root node lines
        line_1 = Line(node_1.get_center() , node_2.get_top()); 
        line_2 = Line(node_1.get_center() , node_3.get_top());

        # Left child lines
        line_3 = Line(node_2.get_center() , node_4.get_top());

        # Right child lines
        line_4 = Line(node_3.get_center() , node_5.get_top());
        line_5 = Line(node_3.get_center() , node_6.get_top());

        self.play(
            ShowCreation(line_1),
            ShowCreation(line_2),
            ShowCreation(line_3),
            ShowCreation(line_4),
            ShowCreation(line_5),
        )
        # Workaround to not having a z-index option
        self.add(node_1, node_2, node_3, node_4, node_5, node_6, 
                 node_1_txt, node_2_txt, node_3_txt, node_4_txt, node_5_txt, node_6_txt
        )

        # -- End of BST Creation --

        # Initial path that Node 3 takes to root
        node_3_path = VMobject()
        node_3_path.set_opacity(0) # Makes path invisible
        node_3_path.set_points_smoothly([*[self.coord(x,y) for x,y in self.path_n3_1]])
        self.add(node_3_path)

        self.wait(1)

        self.play(
            # Makes sure line is attached to node
            UpdateFromFunc(line_1,lambda x: self.update_line(x, node_1, node_2)),
            UpdateFromFunc(line_2,lambda x: self.update_line(x, node_1, node_3)),
            UpdateFromFunc(line_3,lambda x: self.update_line(x, node_2, node_4)),
            UpdateFromFunc(line_4,lambda x: self.update_line(x, node_3, node_5)),
            UpdateFromFunc(line_5,lambda x: self.update_line(x, node_3, node_6)),
            MoveAlongPath(node_3, node_3_path, run_time=1.5)
        )   

        # Root node moving down
        node_1_path = VMobject()
        node_1_path.set_points_smoothly([*[self.coord(x,y) for x,y in self.path_n1_1]])

        # Node 3 moving into root node
        node_3_straight_path = VMobject()
        node_3_straight_path.set_points_smoothly([*[self.coord(x,y) for x,y in self.path_n3_2]])

        for x in [node_1_path, node_3_straight_path]:
            x.set_opacity(0)
            self.add(x)

        self.play(
            UpdateFromFunc(line_1,lambda x: self.update_line(x, node_1, node_2)),
            UpdateFromFunc(line_2,lambda x: self.update_line(x, node_1, node_3)),
            UpdateFromFunc(line_3,lambda x: self.update_line(x, node_2, node_4)),
            UpdateFromFunc(line_4,lambda x: self.update_line(x, node_3, node_5)),
            UpdateFromFunc(line_5,lambda x: self.update_line(x, node_3, node_6)),
            MoveAlongPath(node_1, node_1_path, run_time=1.5),
            MoveAlongPath(node_3, node_3_straight_path, run_time=1.5)
        )

        new_line_2 = Line(node_1.get_top() , node_3.get_center())
        self.play(
            # Node that got reassigned parent
            Transform(line_4, Line(node_1.get_center() , node_5.get_top())),
            # Fixes an ugly looking line
            FadeOut(line_2),
            FadeIn(new_line_2)
        )
        line_2 = new_line_2 

        self.wait(.3)

        # Convert to final tree
        self.play(
            UpdateFromFunc(line_1,lambda x: self.update_line(x, node_1, node_2)),
            UpdateFromFunc(line_2,lambda x: self.update_line(x, node_3, node_1)),
            UpdateFromFunc(line_3,lambda x: self.update_line(x, node_2, node_4)),
            UpdateFromFunc(line_4,lambda x: self.update_line(x, node_1, node_5)),
            UpdateFromFunc(line_5,lambda x: self.update_line(x, node_3, node_6)),
            node_1.move_to, UP * 0 + LEFT * 2.5, 
            node_6.move_to, UP * 0 + RIGHT * 2.5, 
            node_2.move_to, DOWN * 1.5 + LEFT * 4, 
            node_4.move_to, DOWN * 3 + LEFT * 5.5, 
            node_5.move_to, DOWN * 1.5 + LEFT * 0.5, 
        )

        # Workaround to not having a z-index option -- ensures node stays on top of line
        self.add(node_1, node_2, node_3, node_4, node_5, node_6, 
                 node_1_txt, node_2_txt, node_3_txt, node_4_txt, node_5_txt, node_6_txt
        )

        self.wait(3)

    def update_line(self, line, n1, n2):
        # Line "sticks" to node when node moves
        new_line = Line(n1.get_center() , n2.get_top())
        line.become(new_line)
        
    def connect_node(self, node, txt):
        # Makes sure text stays centered on node
        txt.add_updater(lambda m: m.move_to(node.get_center()))

    def make_node(self):
        node = Circle(color=WHITE, radius=0.5, fill_color=WHITE, fill_opacity=1)
        return node

    def make_node_text(self, color, val):
        mytext = TextMobject(val)
        mytext.set_color(color)
        return mytext

    def coord(self,x,y,z=0):
        return np.array([x,y,z])