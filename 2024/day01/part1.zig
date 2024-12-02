const std = @import("std");
const ArrayList = std.ArrayList;
const data = @embedFile("input.txt");
const split = std.mem.split;

pub fn main() anyerror!void {
    var parts = split(u8, data, "\n");
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    //defer gpa.deinit();
    const allocator = gpa.allocator();
    var arr1 = ArrayList(i32).init(allocator);
    defer arr1.deinit();
    var arr2 = ArrayList(i32).init(allocator);
    defer arr2.deinit();

    while (parts.next()) |line| {
        var lineparts = split(u8, line, " ");
        const first = lineparts.next() orelse "";
        var second: []const u8 = "";
        while (second.len <= 0) {
            second = lineparts.next() orelse "EOF";
        }
        try arr1.append(try std.fmt.parseInt(i32, first, 10));
        try arr2.append(try std.fmt.parseInt(i32, second, 10));
    }
    std.mem.sort(i32, arr1.items, {}, comptime std.sort.asc(i32));
    std.mem.sort(i32, arr2.items, {}, comptime std.sort.asc(i32));
    var acc: u32 = 0;
    for (arr1.items, arr2.items) |lhs, rhs| {
        const diff: u32 = @abs(lhs - rhs);
        acc = acc + diff;
    }
    std.debug.print("Result: {d}\n", .{acc});
}
