#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for Line Intersection Application
Лабораторна робота №1 - Варіант 2,6,6

Uses Python's unittest framework for comprehensive testing.
"""

import unittest
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from structures import (
    Line, Point, line_from_two_points, line_perpendicular_to_vector,
    are_lines_parallel, are_lines_coincident, find_intersection
)
from helpers import is_zero, validate_input
from errors import InputValidationError, GeometryError
from constants import MIN_VALUE, MAX_VALUE, EPSILON
from main import analyze_three_lines


class TestUtilityFunctions(unittest.TestCase):
    """Test suite for utility functions"""
    
    def test_is_zero_true(self):
        """Test is_zero returns True for values within epsilon"""
        self.assertTrue(is_zero(0.0))
        self.assertTrue(is_zero(1e-9))
        self.assertTrue(is_zero(-1e-9))
        self.assertTrue(is_zero(EPSILON / 2))
    
    def test_is_zero_false(self):
        """Test is_zero returns False for values outside epsilon"""
        self.assertFalse(is_zero(1e-7))
        self.assertFalse(is_zero(-1e-7))
        self.assertFalse(is_zero(0.1))
        self.assertFalse(is_zero(1.0))
    
    def test_validate_input_value_valid(self):
        """Test validation accepts values within range"""
        # Should not raise exception
        validate_input(MIN_VALUE, "test")
        validate_input(MAX_VALUE, "test")
        validate_input(0, "test")
        validate_input(-100, "test")
        validate_input(100, "test")
    
    def test_validate_input_value_below_min(self):
        """Test validation rejects values below minimum"""
        with self.assertRaises(InputValidationError) as context:
            validate_input(MIN_VALUE - 1, "test_param")
        self.assertIn("test_param", str(context.exception.message))
    
    def test_validate_input_value_above_max(self):
        """Test validation rejects values above maximum"""
        with self.assertRaises(InputValidationError) as context:
            validate_input(MAX_VALUE + 1, "test_param")
        self.assertIn("test_param", str(context.exception.message))


class TestLineFromTwoPoints(unittest.TestCase):
    """Test suite for line_from_two_points function"""
    
    def test_diagonal_line(self):
        """Test creating line y = x through (0,0) and (1,1)"""
        line = line_from_two_points(Point(0, 0), Point(1, 1))
        # y = x => x - y = 0 => A=1, B=-1, C=0
        # (using our formula: A = y2-y1, B = x1-x2, C = y1*x2 - y2*x1)
        self.assertAlmostEqual(line.A, 1)
        self.assertAlmostEqual(line.B, -1)
        self.assertAlmostEqual(line.C, 0)
    
    def test_horizontal_line(self):
        """Test creating horizontal line y = 5"""
        line = line_from_two_points(Point(0, 5), Point(10, 5))
        # A should be 0 (horizontal)
        self.assertTrue(is_zero(line.A))
        self.assertNotEqual(line.B, 0)
    
    def test_vertical_line(self):
        """Test creating vertical line x = 3"""
        line = line_from_two_points(Point(3, 0), Point(3, 10))
        # B should be 0 (vertical)
        self.assertTrue(is_zero(line.B))
        self.assertNotEqual(line.A, 0)
    
    def test_line_through_origin(self):
        """Test line through origin has C = 0"""
        line = line_from_two_points(Point(0, 0), Point(5, 5))
        self.assertTrue(is_zero(line.C))
    
    def test_coincident_points_raises_error(self):
        """Test that coincident points raise GeometryError"""
        with self.assertRaises(GeometryError) as context:
            line_from_two_points(Point(5, 5), Point(5, 5))
        self.assertIn("співпадають", context.exception.message.lower())
    
    def test_boundary_values_left(self):
        """Test with left boundary values"""
        line = line_from_two_points(Point(MIN_VALUE, MIN_VALUE), Point(MIN_VALUE + 1, MIN_VALUE + 1))
        self.assertIsInstance(line, Line)
        self.assertAlmostEqual(line.A, 1)
        self.assertAlmostEqual(line.B, -1)
    
    def test_boundary_values_right(self):
        """Test with right boundary values"""
        line = line_from_two_points(Point(MAX_VALUE, MAX_VALUE), Point(MAX_VALUE - 1, MAX_VALUE - 1))
        self.assertIsInstance(line, Line)
        self.assertAlmostEqual(line.A, -1)
        self.assertAlmostEqual(line.B, 1)


class TestLinePerpendicularToVector(unittest.TestCase):
    """Test suite for line_perpendicular_to_vector function"""
    
    def test_vertical_line_from_horizontal_vector(self):
        """Test creating vertical line (perpendicular to horizontal vector)"""
        # Normal vector (1, 0) creates vertical line x = x0
        line = line_perpendicular_to_vector(Point(5, 10), 1, 0)
        self.assertAlmostEqual(line.A, 1)
        self.assertAlmostEqual(line.B, 0)
        self.assertAlmostEqual(line.C, -5)
    
    def test_horizontal_line_from_vertical_vector(self):
        """Test creating horizontal line (perpendicular to vertical vector)"""
        # Normal vector (0, 1) creates horizontal line y = y0
        line = line_perpendicular_to_vector(Point(10, 5), 0, 1)
        self.assertAlmostEqual(line.A, 0)
        self.assertAlmostEqual(line.B, 1)
        self.assertAlmostEqual(line.C, -5)
    
    def test_diagonal_normal_vector(self):
        """Test with diagonal normal vector"""
        line = line_perpendicular_to_vector(Point(0, 0), -1, 1)
        # a(x - x0) + b(y - y0) = 0 => -x + y = 0
        self.assertAlmostEqual(line.A, -1)
        self.assertAlmostEqual(line.B, 1)
        self.assertAlmostEqual(line.C, 0)
    
    def test_zero_vector_raises_error(self):
        """Test that zero normal vector raises GeometryError"""
        with self.assertRaises(GeometryError) as context:
            line_perpendicular_to_vector(Point(0, 0), 0, 0)
        self.assertIn("нульовим", context.exception.message.lower())
    
    def test_boundary_values(self):
        """Test with boundary values"""
        line = line_perpendicular_to_vector(Point(MIN_VALUE, MAX_VALUE), 1, 1)
        self.assertIsInstance(line, Line)


class TestLineRelationships(unittest.TestCase):
    """Test suite for line relationship functions"""
    
    def test_parallel_horizontal_lines(self):
        """Test parallel detection for horizontal lines"""
        line1 = line_from_two_points(Point(0, 0), Point(10, 0))  # y = 0
        line2 = line_from_two_points(Point(0, 5), Point(10, 5))  # y = 5
        self.assertTrue(are_lines_parallel(line1, line2))
    
    def test_parallel_vertical_lines(self):
        """Test parallel detection for vertical lines"""
        line1 = line_from_two_points(Point(0, 0), Point(0, 10))  # x = 0
        line2 = line_from_two_points(Point(5, 0), Point(5, 10))  # x = 5
        self.assertTrue(are_lines_parallel(line1, line2))
    
    def test_non_parallel_lines(self):
        """Test non-parallel lines are detected correctly"""
        line1 = line_from_two_points(Point(0, 0), Point(10, 0))  # y = 0 (horizontal)
        line2 = line_from_two_points(Point(0, 0), Point(0, 10))  # x = 0 (vertical)
        self.assertFalse(are_lines_parallel(line1, line2))
    
    def test_coincident_lines_diagonal(self):
        """Test coincident detection for diagonal lines"""
        line1 = line_from_two_points(Point(0, 0), Point(1, 1))   # y = x
        line2 = line_from_two_points(Point(2, 2), Point(3, 3))   # y = x (same line)
        self.assertTrue(are_lines_coincident(line1, line2))
    
    def test_coincident_lines_horizontal(self):
        """Test coincident detection for horizontal lines"""
        line1 = line_from_two_points(Point(0, 5), Point(10, 5))  # y = 5
        line2 = line_from_two_points(Point(-5, 5), Point(15, 5))  # y = 5 (same)
        self.assertTrue(are_lines_coincident(line1, line2))
    
    def test_parallel_but_not_coincident(self):
        """Test parallel lines that don't coincide"""
        line1 = line_from_two_points(Point(0, 0), Point(10, 0))  # y = 0
        line2 = line_from_two_points(Point(0, 1), Point(10, 1))  # y = 1
        self.assertTrue(are_lines_parallel(line1, line2))
        self.assertFalse(are_lines_coincident(line1, line2))


class TestFindIntersection(unittest.TestCase):
    """Test suite for find_intersection function"""
    
    def test_intersection_at_origin(self):
        """Test finding intersection at origin"""
        line1 = line_from_two_points(Point(-10, 0), Point(10, 0))  # y = 0
        line2 = line_from_two_points(Point(0, -10), Point(0, 10))  # x = 0
        point = find_intersection(line1, line2)
        self.assertIsNotNone(point)
        self.assertAlmostEqual(point.x, 0)
        self.assertAlmostEqual(point.y, 0)
    
    def test_intersection_diagonal_lines(self):
        """Test intersection of y=x and y=-x"""
        line1 = line_from_two_points(Point(0, 0), Point(1, 1))    # y = x
        line2 = line_from_two_points(Point(0, 0), Point(1, -1))   # y = -x
        point = find_intersection(line1, line2)
        self.assertIsNotNone(point)
        self.assertAlmostEqual(point.x, 0)
        self.assertAlmostEqual(point.y, 0)
    
    def test_parallel_lines_no_intersection(self):
        """Test parallel lines return None"""
        line1 = line_from_two_points(Point(0, 0), Point(10, 0))  # y = 0
        line2 = line_from_two_points(Point(0, 5), Point(10, 5))  # y = 5
        point = find_intersection(line1, line2)
        self.assertIsNone(point)
    
    def test_coincident_lines_no_intersection(self):
        """Test coincident lines return None"""
        line1 = line_from_two_points(Point(0, 0), Point(10, 10))
        line2 = line_from_two_points(Point(1, 1), Point(11, 11))  # same line
        point = find_intersection(line1, line2)
        self.assertIsNone(point)
    
    def test_intersection_at_specific_point(self):
        """Test intersection at a specific point"""
        line1 = line_from_two_points(Point(0, 10), Point(10, 10))  # horizontal y = 10
        line2 = line_from_two_points(Point(5, 0), Point(5, 20))    # vertical x = 5
        point = find_intersection(line1, line2)
        self.assertIsNotNone(point)
        # Horizontal line y=10 and vertical line x=5 intersect at (5, 10)
        self.assertAlmostEqual(point.x, 5)
        self.assertAlmostEqual(point.y, 10)


class TestAnalyzeThreeLinesClass1(unittest.TestCase):
    """Test suite for Class 1: All three lines coincide"""
    
    def test_1_1_left_boundary(self):
        """Test 1.1: All on left boundary"""
        line1 = line_from_two_points(Point(MIN_VALUE, MIN_VALUE), Point(MIN_VALUE + 1, MIN_VALUE + 1))
        line2 = line_perpendicular_to_vector(Point(MIN_VALUE, MIN_VALUE), -1, 1)
        line3 = line_perpendicular_to_vector(Point(MIN_VALUE + 1, MIN_VALUE + 1), -1, 1)
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("співпадають", result.lower())
    
    def test_1_2_right_boundary(self):
        """Test 1.2: All on right boundary"""
        line1 = line_from_two_points(Point(MAX_VALUE - 1, MAX_VALUE - 1), Point(MAX_VALUE, MAX_VALUE))
        line2 = line_perpendicular_to_vector(Point(MAX_VALUE, MAX_VALUE), -1, 1)
        line3 = line_perpendicular_to_vector(Point(MAX_VALUE - 1, MAX_VALUE - 1), -1, 1)
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("співпадають", result.lower())
    
    def test_1_3_middle_values(self):
        """Test 1.3: Typical middle values"""
        line1 = line_from_two_points(Point(0, 0), Point(1, 1))
        line2 = line_perpendicular_to_vector(Point(0, 0), -1, 1)
        line3 = line_perpendicular_to_vector(Point(1, 1), -1, 1)
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("співпадають", result.lower())


class TestAnalyzeThreeLinesClass2(unittest.TestCase):
    """Test suite for Class 2: Lines don't intersect (parallel)"""
    
    def test_2_1_left_boundary(self):
        """Test 2.1: Three parallel horizontal lines - left boundary"""
        line1 = line_from_two_points(Point(MIN_VALUE, MIN_VALUE), Point(MIN_VALUE + 1, MIN_VALUE))
        line2 = line_perpendicular_to_vector(Point(MIN_VALUE, MIN_VALUE + 1), 0, 1)
        line3 = line_perpendicular_to_vector(Point(MIN_VALUE, MIN_VALUE + 2), 0, 1)
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("не перетинаються", result.lower())
    
    def test_2_2_right_boundary(self):
        """Test 2.2: Right boundary"""
        line1 = line_from_two_points(Point(MAX_VALUE - 1, MAX_VALUE), Point(MAX_VALUE, MAX_VALUE))
        line2 = line_perpendicular_to_vector(Point(MAX_VALUE - 1, MAX_VALUE - 1), 0, 1)
        line3 = line_perpendicular_to_vector(Point(MAX_VALUE - 1, MAX_VALUE - 2), 0, 1)
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("не перетинаються", result.lower())
    
    def test_2_3_middle_values(self):
        """Test 2.3: Typical middle values"""
        line1 = line_from_two_points(Point(0, 0), Point(1, 0))
        line2 = line_perpendicular_to_vector(Point(0, 1), 0, 1)
        line3 = line_perpendicular_to_vector(Point(0, -1), 0, 1)
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("не перетинаються", result.lower())


class TestAnalyzeThreeLinesClass3(unittest.TestCase):
    """Test suite for Class 3: Single intersection point"""
    
    def test_3_1_intersection_at_origin(self):
        """Test 3.1: Three lines meet at origin"""
        line1 = line_from_two_points(Point(MIN_VALUE, MIN_VALUE), Point(0, 0))  # y = x
        line2 = line_perpendicular_to_vector(Point(0, 0), 1, 0)  # x = 0
        line3 = line_perpendicular_to_vector(Point(0, 0), 0, 1)  # y = 0
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("єдина точка", result.lower())
        self.assertIn("0.000000", result)
    
    def test_3_2_typical_values(self):
        """Test 3.2: Typical values"""
        line1 = line_from_two_points(Point(MIN_VALUE, 0), Point(MAX_VALUE, 0))  # y = 0
        line2 = line_perpendicular_to_vector(Point(0, MIN_VALUE), 1, 0)  # x = 0
        line3 = line_perpendicular_to_vector(Point(0, 0), 1, 1)  # y = -x
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("єдина точка", result.lower())


class TestAnalyzeThreeLinesClass4(unittest.TestCase):
    """Test suite for Class 4: Two intersection points"""
    
    def test_4_1_two_parallel_one_crossing(self):
        """Test 4.1: Two parallel lines crossed by a third"""
        line1 = line_from_two_points(Point(MIN_VALUE, MIN_VALUE), Point(MIN_VALUE + 1, MIN_VALUE))
        line2 = line_perpendicular_to_vector(Point(MIN_VALUE, MIN_VALUE + 1), 0, 1)
        line3 = line_perpendicular_to_vector(Point(0, MIN_VALUE), 1, 0)
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("дві точки", result.lower())
    
    def test_4_2_typical_values(self):
        """Test 4.2: Typical values"""
        line1 = line_from_two_points(Point(MIN_VALUE, 0), Point(MAX_VALUE, 0))  # y = 0
        line2 = line_perpendicular_to_vector(Point(MIN_VALUE, 1), 0, 1)  # y = 1
        line3 = line_perpendicular_to_vector(Point(0, MIN_VALUE), 1, 0)  # x = 0
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("дві точки", result.lower())


class TestAnalyzeThreeLinesClass5(unittest.TestCase):
    """Test suite for Class 5: Three intersection points"""
    
    def test_5_1_three_different_points(self):
        """Test 5.1: Three different intersection points"""
        line1 = line_from_two_points(Point(MIN_VALUE, 0), Point(MAX_VALUE, 0))  # y = 0
        line2 = line_perpendicular_to_vector(Point(0, MIN_VALUE), 1, 0)  # x = 0
        line3 = line_perpendicular_to_vector(Point(0, 10), 1, 1)  # y = x + 10
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("три точки", result.lower())
    
    def test_5_2_typical_values(self):
        """Test 5.2: Typical values"""
        line1 = line_from_two_points(Point(MIN_VALUE, 50), Point(MAX_VALUE, 50))  # y = 50
        line2 = line_perpendicular_to_vector(Point(30, MIN_VALUE), 1, 0)  # x = 30
        line3 = line_perpendicular_to_vector(Point(0, 0), 1, 1)  # y = x
        result = analyze_three_lines(line1, line2, line3)
        self.assertIn("три точки", result.lower())


class TestInvalidInputClass(unittest.TestCase):
    """Test suite for invalid input handling"""
    
    def test_coincident_points_left_boundary(self):
        """Test НК2.1: Coincident points at left boundary"""
        with self.assertRaises(GeometryError) as context:
            line_from_two_points(Point(MIN_VALUE, MIN_VALUE), Point(MIN_VALUE, MIN_VALUE))
        self.assertIn("співпадають", context.exception.message.lower())
    
    def test_coincident_points_right_boundary(self):
        """Test НК2.2: Coincident points at right boundary"""
        with self.assertRaises(GeometryError) as context:
            line_from_two_points(Point(MAX_VALUE, MAX_VALUE), Point(MAX_VALUE, MAX_VALUE))
        self.assertIn("співпадають", context.exception.message.lower())
    
    def test_coincident_points_middle(self):
        """Test НК2.3: Coincident points at middle"""
        with self.assertRaises(GeometryError) as context:
            line_from_two_points(Point(0, 0), Point(0, 0))
        self.assertIn("співпадають", context.exception.message.lower())
    
    def test_zero_vector_left_boundary(self):
        """Test НК3.1: Zero normal vector at left boundary"""
        with self.assertRaises(GeometryError) as context:
            line_perpendicular_to_vector(Point(MIN_VALUE, MIN_VALUE), 0, 0)
        self.assertIn("нульовим", context.exception.message.lower())
    
    def test_zero_vector_right_boundary(self):
        """Test НК3.2: Zero normal vector at right boundary"""
        with self.assertRaises(GeometryError) as context:
            line_perpendicular_to_vector(Point(MAX_VALUE, MAX_VALUE), 0, 0)
        self.assertIn("нульовим", context.exception.message.lower())
    
    def test_zero_vector_middle(self):
        """Test НК3.3: Zero normal vector at middle"""
        with self.assertRaises(GeometryError) as context:
            line_perpendicular_to_vector(Point(0, 0), 0, 0)
        self.assertIn("нульовим", context.exception.message.lower())
    
    def test_value_below_minimum(self):
        """Test НК1.1: Value below minimum"""
        with self.assertRaises(InputValidationError):
            validate_input(MIN_VALUE - 1, "test")
    
    def test_value_above_maximum(self):
        """Test НК1.2: Value above maximum"""
        with self.assertRaises(InputValidationError):
            validate_input(MAX_VALUE + 1, "test")


class TestSpecialCases(unittest.TestCase):
    """Test suite for special geometric cases"""
    
    def test_line_through_origin_has_c_zero(self):
        """Test СВ1: Line through origin has C = 0"""
        line = line_from_two_points(Point(0, 0), Point(1, 1))
        self.assertTrue(is_zero(line.C))
    
    def test_horizontal_line_has_a_zero(self):
        """Test СВ2: Horizontal line has A ≈ 0"""
        line = line_from_two_points(Point(0, 5), Point(10, 5))
        self.assertTrue(is_zero(line.A))
    
    def test_vertical_line_has_b_zero(self):
        """Test СВ3: Vertical line has B ≈ 0"""
        line = line_from_two_points(Point(5, 0), Point(5, 10))
        self.assertTrue(is_zero(line.B))
    
    def test_x_axis_line(self):
        """Test СВ4: Line on x-axis has A=0, C=0"""
        line = line_from_two_points(Point(0, 0), Point(10, 0))
        self.assertTrue(is_zero(line.A))
        self.assertTrue(is_zero(line.C))
    
    def test_y_axis_line(self):
        """Test СВ5: Line on y-axis has B=0, C=0"""
        line = line_from_two_points(Point(0, 0), Point(0, 10))
        self.assertTrue(is_zero(line.B))
        self.assertTrue(is_zero(line.C))


class TestDataClasses(unittest.TestCase):
    """Test suite for Point and Line data classes"""
    
    def test_point_creation(self):
        """Test Point creation and attributes"""
        p = Point(5.5, -3.2)
        self.assertEqual(p.x, 5.5)
        self.assertEqual(p.y, -3.2)
    
    def test_point_str_representation(self):
        """Test Point string representation"""
        p = Point(1.5, 2.5)
        s = str(p)
        self.assertIn("1.5", s)
        self.assertIn("2.5", s)
    
    def test_line_creation(self):
        """Test Line creation and attributes"""
        line = Line(1, 2, 3)
        self.assertEqual(line.A, 1)
        self.assertEqual(line.B, 2)
        self.assertEqual(line.C, 3)
    
    def test_line_str_representation(self):
        """Test Line string representation"""
        line = Line(1, -2, 3)
        s = str(line)
        self.assertIn("x", s)
        self.assertIn("y", s)


def create_test_suite():
    """Create a test suite with all test cases"""
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestUtilityFunctions,
        TestLineFromTwoPoints,
        TestLinePerpendicularToVector,
        TestLineRelationships,
        TestFindIntersection,
        TestAnalyzeThreeLinesClass1,
        TestAnalyzeThreeLinesClass2,
        TestAnalyzeThreeLinesClass3,
        TestAnalyzeThreeLinesClass4,
        TestAnalyzeThreeLinesClass5,
        TestInvalidInputClass,
        TestSpecialCases,
        TestDataClasses,
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def main():
    """Run all tests with detailed output"""
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass  # If reconfigure fails, continue anyway
    
    # Create test suite
    suite = create_test_suite()
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("ПІДСУМКИ ТЕСТУВАННЯ")
    print("="*70)
    print(f"Виконано тестів: {result.testsRun}")
    print(f"Успішних: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Невдалих: {len(result.failures)}")
    print(f"Помилок: {len(result.errors)}")
    print(f"Пропущено: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✓ ВСІ ТЕСТИ ПРОЙДЕНО УСПІШНО!")
        print("="*70)
        return 0
    else:
        print("\n✗ ДЕЯКІ ТЕСТИ НЕ ПРОЙДЕНО")
        print("="*70)
        return 1


if __name__ == '__main__':
    sys.exit(main())