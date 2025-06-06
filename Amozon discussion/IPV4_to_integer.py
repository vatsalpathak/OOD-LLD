# Convert an IPv4 address (in dot-decimal notation) into its equivalent 32-bit integer value.

# An IPv4 address has 4 octets (A.B.C.D), where:

# Integer Value = A * 256^3 + B * 256^2 + C * 256^1 + D * 256^0
# Input Example:
# "10.0.0.1"

# Output:
# 167772161

class IPConverter:

    def to_integer_brute_force(self, ip: str) -> int:
        parts = ip.split('.')
        result = 0
        power = 3
        for part in parts:
            result += int(part) * (256 ** power)
            power -= 1
        return result

    def to_integer_optimized(self, ip: str) -> int:
        a, b, c, d = map(int, ip.split('.'))
        print(a,b,c,d)
        return (a << 24) | (b << 16) | (c << 8) | d


if __name__ == "__main__":
    ip = "10.0.0.1"
    converter = IPConverter()

    print("Brute Force Result:", converter.to_integer_brute_force(ip))   # ➜ 167772161
    print("Optimized Result:", converter.to_integer_optimized(ip))       # ➜ 167772161
