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

class LShape(VGroup):
    def __init__(self, length, top_point, color=WHITE, **kwargs):
        super().__init__(**kwargs)
        vertical = Line(top_point, np.array([top_point[0], top_point[1] - length, top_point[2]]))
        horizontal = Line(
            np.array([top_point[0], top_point[1] - length, top_point[2]]),
            np.array([top_point[0] + length, top_point[1] - length, top_point[2]]) )
        horizontal.set_color(color)
        vertical.set_color(color)
        l_group = VGroup(vertical, horizontal)
        self.add(l_group)

class PrimitiveVsReference(Scene):
    def setup(self):
        grid = ScreenGrid()
        # self.add(grid)

    def construct(self):
        self.wait(1)

        # Adds title text
        prim_txt = Title("Primitive", -3.9, .1)
        vs_txt = Title("Vs", -1.35, .1)
        ref_txt = Title("Reference", 1.3, .1)
        types_txt = Title("Types", 4.55)
        self.play(
            FadeInFrom(prim_txt, UP),
            FadeInFrom(vs_txt, UP),
            FadeInFrom(ref_txt, UP),
            FadeInFrom(types_txt, UP)
        )
        self.wait(1.5)

        # Moves text into place
        horizontal_line = Line((-7, 2.5, 0), (7, 2.5, 0))
        vertical_line = Line((0, 4, 0), (0, -4, 0))
        self.play(
            Transform(vs_txt, horizontal_line),
            Transform(types_txt, vertical_line),
            prim_txt.move_to, (-3.5, 3.25, 0),
            ref_txt.move_to, (3.5, 3.25, 0),
        )
        self.wait(1)

        # Primitive data types text
        int_txt = TextMobject("Int", fill_color=BLUE)
        int_examples = TextMobject("... -3, -2, -1, 0, 1, 2, 3, ...", fill_color=PINK)
        float_txt = TextMobject("Float", fill_color=BLUE)
        float_examples = TextMobject("... -2.3, -1.5, 0.0, 1.2, 2.9, ...", fill_color=PINK)
        float_examples.scale(0.95)
        boolean_txt = TextMobject("Boolean", fill_color=BLUE)

        boolean_examples = TextMobject("True", "False", fill_color=PINK)
        boolean_examples.arrange(RIGHT, buff=1)

        for elem in [int_txt, float_txt, boolean_txt]:
            elem.scale(1.5)

        int_txt.move_to((-5.55, 2, 0))
        float_txt.move_to((-5.15, 0, 0))
        boolean_txt.move_to((-4.7, -2, 0))

        int_examples.move_to((-3.3, 1, 0))
        float_examples.move_to((-3, -1, 0))
        boolean_examples.move_to((-4.45, -3, 0))

        self.play(
            ShowCreation(int_txt),
            ShowCreation(float_txt),
            ShowCreation(boolean_txt),
            FadeIn(int_examples),
            FadeIn(float_examples),
            FadeIn(boolean_examples),
        )
        self.wait(2)

        # Reference data types text
        array_txt = TextMobject("Array/List", fill_color=BLUE)
        array_examples = TextMobject("[], [1, 2], ['hello', 'world']", fill_color=PINK)

        object_txt = TextMobject("Object", fill_color=BLUE)
        object_examples = TextMobject("School(), Animal(), Dog()", fill_color=PINK)
        
        string_txt = TextMobject("String", fill_color=BLUE)
        string_examples = TextMobject("\"Computer\", \"Science\", \"\"", fill_color=PINK)

        for elem in [array_txt, object_txt, string_txt]:
            elem.scale(1.5)

        array_txt.move_to((2.75, 2, 0))
        object_txt.move_to((2.1, 0, 0))
        string_txt.move_to((2, -2, 0))

        array_examples.move_to((3.7, 1, 0))
        object_examples.move_to((3.85, -1, 0))
        string_examples.move_to((3.9, -3, 0))

        self.play(
            ShowCreation(array_txt),
            ShowCreation(object_txt),
            FadeIn(array_examples),
            FadeIn(object_examples),
        )

        # Delayed String
        self.wait(1)
        self.play(
            ShowCreation(string_txt),
            FadeIn(string_examples),
        )
        self.wait(4.5)

        # String Bounce effect
        self.play(
            string_txt.shift, LEFT * 2,
            string_examples.shift, LEFT * 2,
        )
        self.wait(.5)
        self.play(
            string_txt.shift, RIGHT * 2,
            string_examples.shift, RIGHT * 2,
        )
        self.wait(6)

        group_everything = VGroup(prim_txt, ref_txt, int_txt, int_examples, float_txt, float_examples, boolean_txt, boolean_examples, array_txt, array_examples, object_txt, object_examples, string_txt, string_examples, vs_txt, types_txt)
        question_mark = TextMobject("?")
        question_mark.scale(10)
        self.play(
            Transform(group_everything, question_mark),
        )
        self.wait(2)

        prim_txt = TextMobject("Primitive Types", fill_color=BLUE)
        t_chart_line_horizontal = Line((-3.5, 2.5, 0), (3.5, 2.5, 0))
        t_chart_line_horizontal.set_color(BLUE)
        t_chart_line_vertical = Line((0, 2.5, 0), (0, -4, 0))
        t_chart_line_vertical.set_color(BLUE)
        
        prim_txt.scale(2)
        prim_txt.shift(UP * 3)
        self.play(
            FadeOut(group_everything),
            FadeInFromLarge(prim_txt),
            FadeInFromLarge(t_chart_line_horizontal),
            FadeInFromLarge(t_chart_line_vertical)
        )

        boolean_bits = TextMobject("Boolean" ,"1 bit", fill_color=YELLOW)
        byte_bits = TextMobject("Byte" ,"8 bits", fill_color=YELLOW)
        char_bits = TextMobject("Char" ,"16 bits", fill_color=YELLOW)
        short_bits = TextMobject("Short" ,"16 bits", fill_color=YELLOW)
        int_bits = TextMobject("Int" ,"32 bits", fill_color=YELLOW)
        long_bits = TextMobject("Long" ,"64 bits", fill_color=YELLOW)
        float_bits = TextMobject("Float" ,"32 bits", fill_color=YELLOW)
        double_bits = TextMobject("Double" ,"64 bits", fill_color=YELLOW)
        bits_group = VGroup(boolean_bits, byte_bits, char_bits, short_bits, int_bits, long_bits, float_bits, double_bits)
       
        curr_buffer = 1.85
        for type_bits in bits_group:
            type_bits.arrange(RIGHT, buff=2)
            type_bits.scale(1.4)
            type_bits.shift(UP * curr_buffer)
            curr_buffer -= .75

        self.play(
            ShowCreation(bits_group),
            # Little adjustments
            bits_group[0][0].shift, RIGHT * 0.25,
            bits_group[0][1].shift, LEFT * 0.75,

            bits_group[1][0].shift, LEFT * 0.1,
            bits_group[1][1].shift, LEFT * 0.1,

            bits_group[2][0].shift, RIGHT * 0.1,

            bits_group[3][0].shift, RIGHT * 0.15,
            bits_group[3][1].shift, LEFT * 0.1,

            bits_group[4][0].shift, LEFT * 0.15,
            bits_group[4][1].shift, RIGHT * 0.25,

            bits_group[5][0].shift, RIGHT * 0.15,
            # bits_group[5][1].shift, RIGHT * 0.1,

            bits_group[6][0].shift, RIGHT * 0.15,
            # bits_group[6][1].shift, LEFT * 0.5,

            bits_group[7][0].shift, RIGHT * 0.4,
            bits_group[7][1].shift, LEFT * 0.25,
        )
        self.wait(4)

        int_bits_copy = TextMobject("Int" ,"32 bits", fill_color=YELLOW)
        int_bits_copy.arrange(RIGHT, buff=2)
        int_bits_copy.scale(1.4)
        int_bits_copy.shift(UP * -1.15)
        int_bits_copy[0].shift(LEFT * 0.15)
        int_bits_copy[1].shift(RIGHT * 0.25)

        self.add(int_bits_copy)
        self.play(
            FadeOut(bits_group),
            FadeOut(prim_txt),
            FadeOut(t_chart_line_horizontal),
            FadeOut(t_chart_line_vertical),
            FadeOut(t_chart_line_vertical),
        )

        new_int_bits = TextMobject("Int", "32 bits", fill_color=YELLOW)
        new_int_bits.arrange(RIGHT, buff=.25)
        new_int_bits.move_to((-5, 3, 0))
        self.play(
            Transform(int_bits_copy, new_int_bits)
        )

        self.wait(.3)
        thirtytwo_bits_txt = TextMobject("Int", "32 bits", fill_color=YELLOW)
        thirtytwo_bits_txt.arrange(RIGHT, buff=.25)
        thirtytwo_bits_txt.move_to((-5, 3, 0))
        self.add(thirtytwo_bits_txt)

        bit_boxes = VGroup()
        grid_top = self.make_grid(16, 1)
        for elem in grid_top:
            bit_boxes.add(elem)

        grid_bottom = self.make_grid(16, -1)
        for elem in grid_bottom:
            bit_boxes.add(elem)
        
        self.play(
            Transform(thirtytwo_bits_txt[1], bit_boxes)
        )
        self.add(bit_boxes)
        self.remove(thirtytwo_bits_txt)

        # Code part
        code_border = Rectangle(height=1, width=2.3)
        code_border.move_to((5, 3, 0))
        int_code_txt = TextMobject("int x = 5", fill_color=ORANGE)
        int_code_txt.move_to((5, 3, 0))
        int_code = VGroup(code_border, int_code_txt)
        binary_note = TextMobject("*5 is represented in binary as ","...00000101", fill_color=LIGHT_PINK)
        binary_note[1].set_color(BLUE)
        binary_note.move_to((1.7, 2, 0))
        self.play(
            FadeIn(int_code, run_time=1),
            FadeIn(binary_note, run_time=1)
        )
        self.wait(2)

        # Numbers that go in the boxes
        all_bits = VGroup()
        i = 0
        while i < len(bit_boxes):
            if i == 31 or i == 29:
                one_txt = TextMobject("1", fill_color=ORANGE)
                one_txt.move_to(bit_boxes[i].get_center())
                all_bits.add(one_txt)
            else:
                zero_txt = TextMobject("0")
                zero_txt.move_to(bit_boxes[i].get_center())
                all_bits.add(zero_txt)
            i += 1
        self.play(FadeIn(all_bits))
        self.wait(2)

        # Reference type animation
        ref_bits = TextMobject("Reference", "64 bits", fill_color=YELLOW)
        ref_bits.arrange(RIGHT, buff=.25)
        ref_bits.move_to((-5, 3, 0))
        self.play(
            FadeOut(bit_boxes),
            FadeOut(all_bits),
            FadeOut(code_border),
            FadeOut(int_code_txt),
            FadeOut(binary_note),
            FadeOut(int_bits_copy),
            FadeOut(thirtytwo_bits_txt),
            Transform(new_int_bits, ref_bits),
        )

        self.wait(.3)
        sixtyfour_bits_txt = TextMobject("Reference", "64 bits", fill_color=YELLOW)
        sixtyfour_bits_txt.arrange(RIGHT, buff=.25)
        sixtyfour_bits_txt.move_to((-5, 3, 0))
        self.add(sixtyfour_bits_txt)

        ref_bit_boxes = VGroup()
        grid_one= self.make_grid(16, 1.5)
        for elem in grid_one:
            ref_bit_boxes.add(elem)

        grid_two = self.make_grid(16, 0)
        for elem in grid_two:
            ref_bit_boxes.add(elem)

        grid_three = self.make_grid(16, -1.5)
        for elem in grid_three:
            ref_bit_boxes.add(elem)

        grid_four = self.make_grid(16, -3)
        for elem in grid_four:
            ref_bit_boxes.add(elem)
        
        self.play(
            Transform(sixtyfour_bits_txt[1], ref_bit_boxes)
        )
        self.add(ref_bit_boxes)
        self.remove(sixtyfour_bits_txt)

        # # Code part
        dog_code_border = Rectangle(height=1, width=5)
        dog_code_border.move_to((4.3, 3, 0))
        dog_code_txt = TextMobject("Dog d = new Dog()", fill_color=ORANGE)
        dog_code_txt.move_to((4.3, 3, 0))
        dog_code_txt.scale(0.9)
        dog_code = VGroup(dog_code_border, dog_code_txt)
        dog_binary_note = TextMobject("*The contents of these spaces don't matter to us", fill_color=LIGHT_PINK)
        dog_binary_note.scale(.9)
        dog_binary_note.move_to((1.7, 2.25, 0))
        self.play(
            FadeIn(dog_code, run_time=1),
        )
        self.wait(1)

        # # Numbers that go in the boxes
        all_dog_bits = VGroup()
        i = 0
        while i < len(ref_bit_boxes):
            if random.randint(0, 100) > 50:
                one_txt = TextMobject("1", fill_color=ORANGE)
                one_txt.move_to(ref_bit_boxes[i].get_center())
                all_dog_bits.add(one_txt)
            else:
                zero_txt = TextMobject("0")
                zero_txt.move_to(ref_bit_boxes[i].get_center())
                all_dog_bits.add(zero_txt)
            i += 1
        self.play(FadeIn(all_dog_bits), FadeIn(dog_binary_note, run_time=1))

        # Final code comparison - Primitive
        self.wait(1.75)
        prim_txt = TextMobject("Primitive")
        prim_txt.scale(1.5)
        prim_txt.move_to((-3.5, 3.25, 0)),
        ref_txt = TextMobject("Reference")
        ref_txt.move_to((3.5, 3.25, 0))  
        ref_txt.scale(1.4)

        prim_code = TextMobject("int a = 1") 
        prim_code.scale(1.3)
        prim_code.move_to((-5, 1.5, 0))

        lshape_one = LShape(1, (-3, 2, 0), ORANGE)
        lshape_one_txt = TextMobject("1", fill_color=ORANGE)
        lshape_one_txt.move_to((-2.5, 1.5, 0))

        ref_code = TextMobject("Dog d = Dog()") 
        ref_code.scale(1.1)
        ref_code.move_to((2, 1.5, 0))
        lshape_ref = LShape(1, (4, 2, 0), ORANGE)
        dog_instance_txt = TextMobject("(Dog Instance)", fill_color=PINK)
        dog_instance_txt.move_to((5, 0, 0))
        ref_arrow_one = Arrow(
            np.array([4.5, 1.5, 0]),
            np.array([5.5, 0.25, 0]),
            color=ORANGE
        )

        self.play(
            FadeOut(ref_bit_boxes),
            FadeOut(dog_binary_note),
            FadeOut(dog_code),
            FadeOut(all_dog_bits),
            FadeOut(ref_bits),
            FadeOut(sixtyfour_bits_txt),
            FadeOut(dog_code_txt),
            FadeOut(new_int_bits),

            FadeInFromLarge(vertical_line),
            FadeInFromLarge(horizontal_line),
            FadeInFromLarge(prim_txt),
            FadeInFromLarge(ref_txt),

            FadeIn(prim_code),
            FadeIn(lshape_one),
            FadeIn(lshape_one_txt),

            FadeIn(ref_code),
            FadeIn(lshape_ref),
            FadeIn(dog_instance_txt),
            ShowCreation(ref_arrow_one)
        )

        prim_code_set = TextMobject("int x = a", fill_color=BLUE)
        prim_code_set.scale(1.3)
        prim_code_set.move_to((-5, -1, 0))
        lshape_two = LShape(1, (-3, -0.5, 0), ORANGE)
        lshape_two_txt = TextMobject("1", fill_color=ORANGE)
        lshape_two_txt.move_to((-2.5, -1, 0))
        self.wait(1)
        self.play(
            FadeIn(prim_code_set),
            FadeIn(lshape_two),
            FadeIn(lshape_two_txt),
        )

        no_impact_txt = TextMobject("A change to a won't impact x", fill_color=GREEN)
        no_impact_txt.move_to((-3.5, -2.5, 0))
        self.play(FadeIn(no_impact_txt))

        self.wait(2)
        # Final code comparison - Reference
        ref_code_set = TextMobject("Dog y = d", fill_color=BLUE)
        ref_code_set.scale(1.3)
        ref_code_set.move_to((2, -1, 0))
        lshape_two_ref = LShape(1, (4, -0.5, 0), ORANGE)
        impact_txt = TextMobject("A change to y will impact d", fill_color=RED)
        impact_txt.move_to((3.5, -2.5, 0))
        ref_arrow_two = Arrow(
            np.array([4.5, -1, 0]),
            np.array([5.5, -0.25, 0]),
            color=ORANGE
        )
        self.play(
            FadeIn(ref_code_set),
            FadeIn(lshape_two_ref),
            FadeIn(impact_txt),
            ShowCreation(ref_arrow_two)
        )


        self.wait(5)


    def make_grid(self, n, y):
        length = 10 / n
        square_one = Square(side_length=length)
        square_one.move_to((-7+(length - .2), y, 0))
        squares = [square_one]
        for i in range(1, n):
            sq = Square(side_length=length)
            sq.next_to(squares[i - 1])
            squares.append(sq)
        return squares
        