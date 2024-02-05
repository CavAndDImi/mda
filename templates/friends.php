<!DOCTYPE html>
<html lang="en">

<head>
    <title>Birth of Artemis</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="keywords" content="crypto, nss, space, genesis">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/mystyle_page.css') }}">
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
</head>

<body method="post">
    <script src="{{url_for('static', filename='Scripturi/script_log.js')}}"></script>
    <div class="navbar">
        <div class="logo"><a href="">Birth Of Artemis</a></div>
        <button class="wallet" onClick="check_wallet()">Balance: {{account['wallet']}}</button>
    </div>


    <div class="dop">
        <form method="post">
            <table>
                <thead>
                    <tr>
                        <th>Username</th>

                    </tr>
                </thead>
                <tbody>
                    {% for item in dap %}
                    <tr>
                        <td><input id="nume" style="display: none" value="{{item['cnp']}}">{{item['username']}}</input>
                        </td>
                        <td><input id="poz({{item['cnp']}})" type="button" value="Accept"></input></td>
                        <td><input id="neg({{item['cnp']}})" type="button" value="Deny"></input></td>

                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </form>
    </div>
    <div class="pot">
        <table>
            <thead>
                <tr>
                    <th>Friend</th>
                    <th>Balance</th>
                </tr>
            </thead>
            <tbody>
                {% for item in entries %}
                <tr>
                    <td>{{item['friend2']}}</td>
                    <td>{{item['wallet']}}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    <div class="frequest">
        <button type="sex" id="addF" onclick="addF()" value="0">Add friend</button>
        <br><br>
        <form method="post">
            <input id="addFr" style="display: none" placeholder="Search for friend" class="textbox"
                name="addFr"></input>
            <input type="submit" id="addFrSub" style="display: none" name="adFr"
                placeholder="Send Friend Request"></input>
        </form>
        <div class="msg" id="msg" style="display: none">{{msg}}</div>
    </div>
    <div class="frumi">
        <h2>{{account['username']}}</h2>
    </div>
</body>

</html>