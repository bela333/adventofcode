const std = @import("std");
const ArrayList = std.ArrayList;
const data = @embedFile("input.txt");
const split = std.mem.split;

pub fn main() anyerror!void {
    var parts = split(u8, data, "\n");
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    //defer gpa.deinit();
    const allocator = gpa.allocator();
    var lhs_count = std.AutoHashMap(u32, u32).init(allocator);
    defer lhs_count.deinit();
    var rhs_count = std.AutoHashMap(u32, u32).init(allocator);
    defer rhs_count.deinit();

    while (parts.next()) |line| {
        var lineparts = split(u8, line, " ");
        const lhs = lineparts.next() orelse "";
        var rhs: []const u8 = "";
        while (rhs.len <= 0) {
            rhs = lineparts.next() orelse "EOF";
        }
        const nlhs = try std.fmt.parseInt(u32, lhs, 10);
        const nrhs = try std.fmt.parseInt(u32, rhs, 10);
        const lhsval = lhs_count.get(nlhs) orelse 0;
        try lhs_count.put(nlhs, lhsval + 1);
        const rhsval = rhs_count.get(nrhs) orelse 0;
        try rhs_count.put(nrhs, rhsval + 1);
    }
    var acc: u32 = 0;
    var lhsit = lhs_count.iterator();
    while (lhsit.next()) |entry| {
        const lhsn = entry.value_ptr.*;
        const rhsn = rhs_count.get(entry.key_ptr.*) orelse 0;
        const val = lhsn * rhsn * entry.key_ptr.*;
        acc += val;
    }
    std.debug.print("Result: {d}\n", .{acc});
}
