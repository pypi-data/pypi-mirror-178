Fantable - Table Builder For Python
============================================================

Author: [Sptty Chan (Fanda\)](https://www.facebook.com/profile.php?id=100024425583446)

Github & Examples: https://github.com/sptty-chan/fantable


Example:

    from fantable import Table # import

    create_table = Table(title="Daftar Hero Mobile Legends") # Title hanya optional
    create_table.column("no", "nama hero", "role", "tipe damage") # Set Column
    create_table.tab_row("01", "gusion", "assasin", "magic damage") # Menambah baris
    create_table.tab_row("02", "kagura", "mage", "magic damage")
    create_table.tab_row("03", "jhonson", "tank", "magic damage")
    create_table.tab_row("04", "lesley", "marksman", "phisical damage")
    create_table.commit() # Commit table
    print(create_table) # Print table
