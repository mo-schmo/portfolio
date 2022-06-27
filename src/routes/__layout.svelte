<nav class="header">
    <a class="active" href="/">Home</a>
    <a href="/about">About</a>
    <a target="_blank" href="https://www.github.com/mo-schmo">
        <i class="fa fa-github github"></i>
    </a>
</nav>

<slot></slot>

<style>
    .header {
        overflow: hidden;
        background-color: #f1f1f1;
        padding: 20px 10px;
    }

    .header a {
        float: left;
        color: black;
        text-align: center;
        padding: 12px;
        text-decoration: none;
        font-size: 18px;
        line-height: 25px;
        border-radius: 4px;
    }

    .header a:hover {
        background-color: #ddd;
        color: black;
    }

    .header a.active {
        background-color: dodgerblue;
        color: white;
    }

    .github {
        font-size: 40px;
    }

    @media screen and (max-width: 500px) {
        .header a {
            float: none;
            display: block;
            text-align: left;
        }
    }
</style>