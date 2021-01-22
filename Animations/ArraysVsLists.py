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
    def __init__(self, text, x, y=0, **kwargs):
        super().__init__(**kwargs)
        txt = TextMobject(text)
        txt.move_to(np.array([x, y, 0]))
        txt.scale(1.75)
        self.add(txt)

class Arrays(Scene):
    def construct(self):
        grid = ScreenGrid()
        self.add(grid)
        self.wait(.3)

        # Adds title text
        arrays_title_txt = Title("Arrays", -3.2, .1)
        vs_txt = Title("Vs", 0, .1)
        lists_title_txt = Title("Lists", 2.8, .1)
        arrays_title_txt.scale(1.5)
        vs_txt.scale(1.5)
        lists_title_txt.scale(1.5)

        self.play(
            FadeInFrom(arrays_title_txt, UP),
            FadeInFrom(vs_txt, UP),
            FadeInFrom(lists_title_txt, UP),
        )
        self.wait(3.5)
        horizontal_line = Line((-7, 2.5, 0), (7, 2.5, 0))
        vertical_line = Line((0, 4, 0), (0, -4, 0))
        self.play(
            Transform(vs_txt, horizontal_line),
            FadeIn(vertical_line),
            arrays_title_txt.move_to, (-3.5, 3.25, 0),
            lists_title_txt.move_to, (3.5, 3.25, 0),
        )
        self.wait(2)

        arrays_example = TextMobject("[1, 2, 3, 4, 5]")
        arrays_example.move_to((-3.5, 1, 0))
        arrays_example.scale(1.5)
        self.play(ShowCreation(arrays_example))

        types_text = TextMobject("* All are ", "int","s", fill_color=ORANGE)
        types_text.scale(1.3)
        types_text[1].set_color(BLUE)
        types_text.move_to((-3.5, -1, 0))
        self.play(FadeIn(types_text))        
        self.wait(3)

        list_example = TextMobject("[1, `hi', [5, `hey'], Octopus()]")
        list_example.move_to((3.5, 1, 0))
        list_example.scale(1)
        self.play(ShowCreation(list_example))
        self.wait(2)

        array_declaration = TextMobject("int[5] = new int[5]", fill_color=BLUE)
        array_declaration.scale(1.4)
        array_declaration.move_to((-3.5, 1.3, 0))
        self.play(
            FadeOut(types_text),
            FadeIn(array_declaration),
            arrays_example.shift, DOWN,
            arrays_example.set_color, '#66ff00',
        )
        self.wait(1)

        invalid_example1 = TextMobject("[1, 2, 3, 4, 5, 6]", fill_color='#ff0000')
        invalid_example2 = TextMobject("[1, 2, Dog(), 3, 4]", fill_color='#ff0000')
        invalid_example1.scale(1.4)
        invalid_example2.scale(1.4)
        invalid_example1.move_to((-3.5, -1, 0))
        invalid_example2.move_to((-3.5, -2, 0))
        self.play(
            FadeIn(invalid_example1),
            FadeIn(invalid_example2),
        )

        list_declaration = TextMobject("x = []", fill_color=BLUE)
        list_declaration.scale(1.4)
        list_declaration.move_to((3.5, 1.3, 0))
        self.wait(2)
        valid_example1 = TextMobject("[1, 2, 3, 4, 5, 6]", fill_color='#66ff00')
        valid_example2 = TextMobject("[1, 2, Dog(), 3, 4]", fill_color='#66ff00')
        valid_example1.scale(1.4)
        valid_example2.scale(1.4)
        valid_example1.move_to((3.5, -1, 0))
        valid_example2.move_to((3.5, -2, 0))
        self.play(
            FadeIn(list_declaration),
            list_example.shift, DOWN,
            list_example.set_color, '#66ff00',
            FadeIn(valid_example1),
            FadeIn(valid_example2)
        )
        self.wait(3)

        dynamic_size_txt = TextMobject("Dynamic Sizing")
        dynamic_size_txt.scale(1.5)
        dynamic_size_txt.shift(UP * 3.25)
        what_we_see_txt = TextMobject("What we see", fill_color=MAROON_C)
        bts_txt = TextMobject("Behind the scenes", fill_color=YELLOW)
        what_we_see_txt.scale(1.5)
        bts_txt.scale(1.5)
        what_we_see_txt.move_to((-3.5, 2, 0))
        bts_txt.move_to((3.5, 2, 0))
        self.play(
            FadeOut(arrays_title_txt),
            FadeOut(lists_title_txt),
            FadeOut(list_example),
            FadeOut(arrays_example),
            FadeOut(array_declaration),
            FadeOut(list_declaration),
            FadeOut(invalid_example1),
            FadeOut(invalid_example2),
            FadeOut(valid_example2),
            FadeOut(valid_example1),
            FadeOut(vs_txt),
            vertical_line.shift, DOWN * 2.5,
            horizontal_line.shift, DOWN * 1,
            FadeInFrom(dynamic_size_txt, UP),
            FadeInFrom(bts_txt, UP),
            FadeInFrom(what_we_see_txt, UP),
        )
        self.wait(.3)

        us_list_box_1 = Square(side_length=1.3)
        us_list_box_1.move_to((-5.3, 0, 0))
        us_list_txt_1 = TextMobject("1", fill_color=BLUE)
        us_list_txt_1.scale(2)
        us_list_txt_1.move_to(us_list_box_1.get_center())

        bts_list_box_1 = Square(side_length=1.3)
        bts_list_box_1.move_to((1.7, 0, 0))
        bts_list_box_2 = Square(side_length=1.3)
        bts_list_box_2.move_to((3.5, 0, 0))
        bts_list_box_3 = Square(side_length=1.3)
        bts_list_box_3.move_to((5.3, 0, 0))
        
        bts_list_txt_1 = TextMobject("1", fill_color=BLUE)
        bts_list_txt_1.scale(2)
        bts_list_txt_1.move_to(bts_list_box_1.get_center())

        self.play(
            ShowCreation(us_list_box_1),
            ShowCreation(bts_list_box_1),
            ShowCreation(bts_list_box_2),
            ShowCreation(bts_list_box_3),
            FadeIn(us_list_txt_1),
            FadeIn(bts_list_txt_1)
        )
        self.wait(.5)        
        us_list_box_2 = Square(side_length=1.3)
        us_list_box_2.move_to((-3.5, 0, 0))
        us_list_box_3 = Square(side_length=1.3)
        us_list_box_3.move_to((-1.7, 0, 0))

        us_list_txt_2 = TextMobject("2", fill_color=RED_E)
        us_list_txt_2.scale(2)
        us_list_txt_2.move_to(us_list_box_2.get_center())
        bts_list_txt_2 = TextMobject("2", fill_color=RED_E)
        bts_list_txt_2.scale(2)
        bts_list_txt_2.move_to(bts_list_box_2.get_center())
        self.play(
            ShowCreation(us_list_box_2),
            FadeIn(us_list_txt_2),
            FadeIn(bts_list_txt_2),
        )
        self.wait(0.5)
        us_list_txt_3 = TextMobject("3", fill_color=TEAL_D)
        us_list_txt_3.scale(2)
        us_list_txt_3.move_to(us_list_box_3.get_center())
        bts_list_txt_3 = TextMobject("3", fill_color=TEAL_D)
        bts_list_txt_3.scale(2)
        bts_list_txt_3.move_to(bts_list_box_3.get_center())
        self.play(
            ShowCreation(us_list_box_3),
            FadeIn(us_list_txt_3),
            FadeIn(bts_list_txt_3),
        )

        # The row that will be transformed
        bts_list_box_1_copy = Square(side_length=1.3)
        bts_list_box_1_copy.move_to((1.7, 0, 0))
        bts_list_box_2_copy = Square(side_length=1.3)
        bts_list_box_2_copy.move_to((3.5, 0, 0))
        bts_list_box_3_copy = Square(side_length=1.3)
        bts_list_box_3_copy.move_to((5.3, 0, 0))
        bts_row_1_copy = VGroup(bts_list_box_1_copy, bts_list_box_2_copy, bts_list_box_3_copy) 
        self.add(bts_row_1_copy)

        self.wait(2)
        bts_list_box_4 = Square(side_length=1.3)
        bts_list_box_4.move_to((1.7, -2, 0))
        bts_list_box_5 = Square(side_length=1.3)
        bts_list_box_5.move_to((3.5, -2, 0))
        bts_list_box_6 = Square(side_length=1.3)
        bts_list_box_6.move_to((5.3, -2, 0))
        bts_row_2 = VGroup(bts_list_box_4, bts_list_box_5, bts_list_box_6)

        # Second "What we see" row
        us_list_box_6 = Square(side_length=1.3)
        us_list_box_6.move_to((-1.7, -2, 0))
        us_list_box_5 = Square(side_length=1.3)
        us_list_box_5.move_to((-3.5, -2, 0))
        us_list_box_4 = Square(side_length=1.3)
        us_list_box_4.move_to((-5.3, -2, 0))

        us_list_txt_4 = TextMobject("4", fill_color=MAROON_C)
        us_list_txt_4.scale(2)
        us_list_txt_4.move_to(us_list_box_4.get_center())
        bts_list_txt_4 = TextMobject("4", fill_color=MAROON_C)
        bts_list_txt_4.scale(2)
        bts_list_txt_4.move_to(bts_list_box_4.get_center())
        self.play(
            Transform(bts_row_1_copy, bts_row_2),
            ShowCreation(us_list_box_4),
            FadeIn(us_list_txt_4),
            FadeIn(bts_list_txt_4)
        )
        self.wait(.3)

        us_list_txt_5 = TextMobject("5", fill_color=YELLOW_E)
        us_list_txt_5.scale(2)
        us_list_txt_5.move_to(us_list_box_5.get_center())
        bts_list_txt_5 = TextMobject("5", fill_color=YELLOW_E)
        bts_list_txt_5.scale(2)
        bts_list_txt_5.move_to(bts_list_box_5.get_center())
        self.play(
            ShowCreation(us_list_box_5),
            FadeIn(us_list_txt_5),
            FadeIn(bts_list_txt_5),
        )
        self.wait(.3)

        us_list_txt_6 = TextMobject("6", fill_color=BLUE_B)
        us_list_txt_6.scale(2)
        us_list_txt_6.move_to(us_list_box_6.get_center())
        bts_list_txt_6 = TextMobject("6", fill_color=BLUE_B)
        bts_list_txt_6.scale(2)
        bts_list_txt_6.move_to(bts_list_box_6.get_center())
        self.play(
            ShowCreation(us_list_box_6),
            FadeIn(us_list_txt_6),
            FadeIn(bts_list_txt_6),
        )
        self.wait(1.5)
        
        us_bottom_row = VGroup(us_list_box_4, us_list_box_5, us_list_box_6, us_list_txt_4, us_list_txt_5, us_list_txt_6)
        us_top_row = VGroup(us_list_box_1, us_list_box_2, us_list_box_3, us_list_txt_1, us_list_txt_2, us_list_txt_3)
        self.play(
            FadeOut(bts_row_1_copy),
            FadeOut(bts_list_box_1),
            FadeOut(bts_list_box_2),
            FadeOut(bts_list_box_3),
            FadeOut(bts_list_txt_1),
            FadeOut(bts_list_txt_2),
            FadeOut(bts_list_txt_3),
            FadeOut(bts_list_txt_4),
            FadeOut(bts_list_txt_5),
            FadeOut(bts_list_txt_6),
            FadeOut(bts_txt),
            FadeOut(what_we_see_txt),
            FadeOut(horizontal_line),
            FadeOut(vertical_line),
            FadeOut(dynamic_size_txt),
            us_bottom_row.shift, (RIGHT * 6.25) + (UP * 2), run_time=1.5,
        )
        self.play(
            us_top_row.shift, (RIGHT * .75), run_time=.2,
        )
        self.wait(.3)
        zero_index_txt = TextMobject("0")
        zero_index_txt.move_to((-4.5, -1.5, 0))
        one_index_txt = TextMobject("1")
        one_index_txt.move_to((-2.75, -1.5, 0))
        two_index_txt = TextMobject("2")
        two_index_txt.move_to((-1, -1.5, 0))
        three_index_txt = TextMobject("3")
        three_index_txt.move_to((1, -1.5, 0))
        four_index_txt = TextMobject("4")
        four_index_txt.move_to((2.75, -1.5, 0))
        five_index_txt = TextMobject("5")
        five_index_txt.move_to((4.5, -1.5, 0))
        index_txts = VGroup(zero_index_txt, one_index_txt, two_index_txt, three_index_txt, four_index_txt, five_index_txt)
        for idx in index_txts:
            idx.scale(2)
            self.play(FadeIn(idx, run_time=0.5))
        self.wait(1.5)

        full_arr_with_indices = VGroup(us_bottom_row, us_top_row, index_txts)
        self.play(
            full_arr_with_indices.shift, UP * 2.5
        )

        accessing_txt_0 = TextMobject("nums[0] = ")
        accessing_txt_0.move_to((-2.5, -1, 0))
        accessing_txt_1 = TextMobject("nums[1] = ")
        accessing_txt_1.move_to((-2.5, -2, 0))
        accessing_txt_2 = TextMobject("nums[2] = ")
        accessing_txt_2.move_to((-2.5, -3, 0))
        accessing_txt_3 = TextMobject("nums[3] = ")
        accessing_txt_3.move_to((2.5, -1, 0))
        accessing_txt_4 = TextMobject("nums[4] = ")
        accessing_txt_4.move_to((2.5, -2, 0))
        accessing_txt_5 = TextMobject("nums[5] = ")
        accessing_txt_5.move_to((2.5, -3, 0))
        accessing_txts = VGroup(accessing_txt_0, accessing_txt_1, accessing_txt_2, accessing_txt_3, accessing_txt_4, accessing_txt_5)

        nums_txt = TextMobject("nums:")
        nums_txt.move_to((-6, 2.5, 0))
        for elem in accessing_txts:
            elem.scale(1.5)
        self.play(
            FadeIn(accessing_txts),
            FadeIn(nums_txt)
        )

        correct_access_1 = TextMobject("1", fill_color=BLUE)
        correct_access_2 = TextMobject("2", fill_color=RED_E)
        correct_access_3 = TextMobject("3", fill_color=TEAL_D)
        correct_access_4 = TextMobject("4", fill_color=MAROON_C)
        correct_access_5 = TextMobject("5", fill_color=YELLOW_E)
        correct_access_6 = TextMobject("6", fill_color=BLUE_B)
        correct_access_1.next_to(accessing_txt_0, buff=0.5)
        correct_access_2.next_to(accessing_txt_1, buff=0.5)
        correct_access_3.next_to(accessing_txt_2, buff=0.5)
        correct_access_4.next_to(accessing_txt_3, buff=0.5)
        correct_access_5.next_to(accessing_txt_4, buff=0.5)
        correct_access_6.next_to(accessing_txt_5, buff=0.5)
        correct_accesses = VGroup(correct_access_1, correct_access_2, correct_access_3, correct_access_4, correct_access_5, correct_access_6)
        for elem in correct_accesses:
            elem.scale(1.5)
        self.play(
            FadeIn(correct_accesses)
        )
        self.wait(2)

        self.play(
            FadeOut(index_txts),
            FadeOut(correct_accesses),
            FadeOut(accessing_txts),
        )
        self.wait(1)

        nums_copy_txt = TextMobject("numsTwo = nums")
        nums_copy_txt.scale(1.3)
        nums_copy_txt.move_to((-4, 0, 0))
        self.play(FadeIn(nums_copy_txt))
        arrow_to_nums = Arrow(
            np.array([-2, 0.25, 0]),
            np.array([-6, 2, 0]),
        )
        arrow_to_nums.set_color(ORANGE)
        self.play(
            ShowCreation(arrow_to_nums)
        )


        self.wait(6)
    