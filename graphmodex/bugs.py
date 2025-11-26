BUGS = [
    {
        "id": "BUG-0001",
        "title": "main_layout has no **kwargs in the function",
        "status": "open",
        "module": "plotlymodex/layout/subplot.py",
        "details": "Problems may arrise when wanting to passing extra keyword arguments to main_layout function (such as customdata = 'no' or more in depth specifications). Therefore, we need to add flexibility to some inner definitions.",
    },
]