# You're given an array of t-shirt sizes: "s", "m", "l". You need to sort them in-place to be in this order: small, medium, large.

# Example:
# Input:
# clothes = ["l", "s", "l", "m", "m", "s"]
# Output:
# ["s", "s", "m", "m", "l", "l"]


class TShirtSorter:
    def sort_by_counting(self, clothes):
        count = {"s" : 0, "m" : 0, "l" : 0}

        for cloth in clothes:
            count[cloth] += 1
        
        i = 0
        for size in ["s","m","l"]:
            for _ in range(count[size]):
                clothes[i] = size
                i+=1
        return clothes

    def sort_by_dnf(self, clothes):
        low = 0
        mid = 0
        high = len(clothes) - 1

        while mid <= high:
            if clothes[mid] == 's':
                clothes[low], clothes[mid] = clothes[mid],clothes[low]
                mid += 1
                low += 1
            elif clothes[mid] == 'm':
                mid += 1
            else:
                clothes[mid],clothes[high] = clothes[high],clothes[mid]
                high -=1
        return clothes

# ------------------ Test Code ------------------

if __name__ == "__main__":
    sorter = TShirtSorter()

    clothes1 = ["l", "s", "l", "m", "m", "s"]
    clothes2 = ["l", "s", "l", "m", "m", "s"]

    print("Original Clothes:", clothes1)

    print("\n Sort by Counting:")
    print(sorter.sort_by_counting(clothes1))  

    print("\n Sort by DNF (Dutch National Flag):")
    print(sorter.sort_by_dnf(clothes2))   