import pytest
import sys
sys.path.append('../')
from helpers.serialization import serialize, deserialize

def test_signup():
    # _____________JSON MODE_____________
    # Typical Case
    data = {"command": "signup", "username": "test", "password": "test"}
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Test and Password
    data = {"command": "signup", "username": "", "password": ""}
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username and Password
    data = {
        "command": "signup", 
        "username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
        "password": "ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]]"
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {"command": "signup", "username": "test", "password": "test"}
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Test and Password
    data = {"command": "signup", "username": "", "password": ""}
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username and Password
    data = {
        "command": "signup", 
        "username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
        "password": "ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]]"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

def test_login():
    # _____________JSON MODE_____________
    # Typical Case
    data = {"command": "login", "username": "test", "password": "test"}
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Test and Password
    data = {"command": "login", "username": "", "password": ""}
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username and Password
    data = {
        "command": "login", 
        "username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
        "password": "ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]]"
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {"command": "login", "username": "test", "password": "test"}
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Test and Password
    data = {"command": "login", "username": "", "password": ""}
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username and Password
    data = {
        "command": "login", 
        "username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
        "password": "ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]] ahbo   q24903thpghbawp9e0ghq092hgpwhvaoweghq29ghpq2ewghaweoigh;q23htgqp2309g8ehqwp9ghq20493t8hgqwpe9aghewp9gih;3OIH    [3GHpwq938hgpw9aehgqw4890htg[   2qh390p8HE4[    2390H2-948EHp9wh3-2hp   09q3ghq9    83ht0[9hgas;doighq0948yh    -40ehgP_)*(w4y-thgpa0ehs8(ehtq83p40hgyp98qHWQRQ){(h[tjg;2qt0h34tpqw890rfh[we;GHIO   P30Q8rhA_Wf9gh[Q309HT   -2yrgq-e8hwp30HT-q3ty-T39H  ;qhtg093Y-tphg3p9Q03YR5-    0HT2P98q3gt -yp8Q0GET-q8y3h5rp089WTG-q95yhr[p0QTEHpq38hrpQ9TGYH[T093htp-QY3T4HP;3IHRG-  9uh[q0tgh3p9H34TP*43th;.4KTEGQ_8YP9HIO;3T2kleqfADV*9upijo;kl    r3wefaDG689YOUHINPJ KREAGS7Y08HU9PIJONKR4   LEWFQdw7y089upijoky5wthsg08y9uo94TQ3908 8-Y--08 2uy3-   y4t-h   -ytp349htnogare0y89hpuqio4tghawer098thupq4njweagh89pioq4nwtaes980pohuilwakety809pohi3t4weYG8-HP0IOUAOHIGhhopaiohgoiuhfgoiqhuithgawperghapi hwhtpaoih paowutpoaiewub apowieut paoweiut apoiupaoebiut paosiutpaowe8utpaw9834yt8wqy4ptioaepsogiHRtirpotiuseportuypaowreytpoiqw4tj op]]]]]])})]]]]"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

def test_delete_account():
    # _____________JSON MODE_____________
    # Typical Case
    data = {"command": "delete_account", "username": "test"}
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Test and Password
    data = {"command": "delete_account", "username": ""}
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username and Password
    data = {
        "command": "delete_account", 
        "username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {"command": "delete_account", "username": "test"}
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Test and Password
    data = {"command": "delete_account", "username": ""}
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username and Password
    data = {
        "command": "delete_account", 
        "username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"
    
def test_logout():
    # Typical Case
    data = {"command": "logout", "username": "test"}
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Test and Password
    data = {"command": "logout", "username": ""}
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username and Password
    data = {
        "command": "logout", 
        "username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {"command": "logout", "username": "test"}
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Test and Password
    data = {"command": "logout", "username": ""}
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username and Password
    data = {
        "command": "logout", 
        "username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"
    
def test_list():
    # Typical Case
    data = {"command": "list", "username_pattern": "test"}
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Username Pattern
    data = {"command": "list", "username_pattern": ""}
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username Pattern
    data = {
        "command": "list", 
        "username_pattern": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {"command": "list", "username_pattern": "test"}
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Username Pattern
    data = {"command": "list", "username_pattern": ""}
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username Pattern
    data = {
        "command": "list", 
        "username_pattern": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"
    
def test_message():
    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "message", 
        "sender_username": "test", 
        "target_username": "test2", 
        "message": "Hello",
        "timestamp": 1234567890
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Sender Username
    data = {
        "command": "message", 
        "sender_username": "", 
        "target_username": "test2", 
        "message": "Hello",
        "timestamp": 1234567890
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Target Username
    data = {
        "command": "message", 
        "sender_username": "test", 
        "target_username": "", 
        "message": "Hello",
        "timestamp": 1234567890
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Message
    data = {
        "command": "message", 
        "sender_username": "test", 
        "target_username": "test2", 
        "message": "",
        "timestamp": 1234567890
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Sender Username
    data = {
        "command": "message", 
        "sender_username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
        "target_username": "test2", 
        "message": "Hello",
        "timestamp": 1234567890
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"
    

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "message", 
        "sender_username": "test", 
        "target_username": "test2", 
        "message": "Hello",
        "timestamp": 1234567890
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Sender Username
    data = {
        "command": "message", 
        "sender_username": "", 
        "target_username": "test2", 
        "message": "Hello",
        "timestamp": 1234567890
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Target Username
    data = {
        "command": "message", 
        "sender_username": "test", 
        "target_username": "", 
        "message": "Hello",
        "timestamp": 1234567890
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Message
    data = {
        "command": "message", 
        "sender_username": "test", 
        "target_username": "test2", 
        "message": "",
        "timestamp": 1234567890
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Sender Username
    data = {
        "command": "message", 
        "sender_username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
        "target_username": "test2", 
        "message": "Hello",
        "timestamp": 1234567890
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

def test_register():
    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "register", 
        "username": "test", 
        "host": "127.0.0.1",
        "port": 54400
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Username
    data = {
        "command": "register", 
        "username": "test", 
        "host": "127.0.0.1",
        "port": 54400
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username
    data = {
        "command": "register", 
        "username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
        "host": "127.0.0.1",
        "port": 54400
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "register", 
        "username": "test", 
        "host": "127.0.0.1",
        "port": 54400
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Username
    data = {
        "command": "register", 
        "username": "test", 
        "host": "127.0.0.1",
        "port": 54400
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Long Username
    data = {
        "command": "register", 
        "username": "qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqwegqwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg    qwiejgpqoijgpqowiegjqwpoeigqwegqppoqiehgpqhwegihqwepgqwegpiqwehpgoihqwgohqwpgohqwepoighqwepighqpweoighqpoweighqwpoeighqwepgohqwepgoihqwegpohqwegpoihqwegpoihqwegpoihqwegpohqwegpoihqwegpoihqwegpoqwiehgqpwoeighqwepoghqwpoeghpoqweighpoqwieghqpwoeighqwpeogihqwepoghiqwepogihqwepogihqwpoeghqpowieghpqowieghqpoweighqwpoeighqwepogihqwepogihqwepoghiqwepoghiqwepogiqwpoeghpqowihegpoqwihegpoqwhegiqpowegihqpoeighqwpeoghiqwepgoqewgpohqwegpoihqwegpohiqwegoihpqwegpohiqwegihoqwgeohqwgeohgwqehwgehqqwpogweohgweogihqewioghqopiewghqpiowegpqweiogpqowehgoqpiweghpoihgpohqwegopiqwegpohqwepgoqpwoehgqpewighqwepgohqewgpqweg", 
        "host": "127.0.0.1",
        "port": 54400
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

def test_read():
    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "read", 
        "username": "test",
        "num_messages": 10
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # No Messages
    data = {
        "command": "read", 
        "username": "test",
        "num_messages": 0
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"
    
    # Large Number of Messages
    data = {
        "command": "read", 
        "username": "test",
        "num_messages": 1000
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Username
    data = {
        "command": "read", 
        "username": "",
        "num_messages": 10
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "read", 
        "username": "test",
        "num_messages": 10
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # No Messages
    data = {
        "command": "read", 
        "username": "test",
        "num_messages": 0
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Large Number of Messages
    data = {
        "command": "read", 
        "username": "test",
        "num_messages": 1000
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Username
    data = {
        "command": "read", 
        "username": "",
        "num_messages": 10
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Number of Messages is a string
    data = {
        "command": "read", 
        "username": "test",
        "num_messages": "d"
    }

    true_result = {
        "command": "read", 
        "username": "test",
        "num_messages": 0
    }
    
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == true_result, f"Deserialization failed for data: {data}"

def test_delete_message():
    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "delete_message", 
        "username": "test",
        "message_id": "69ee4fc7-8432-40da-99d4-1713e208b568"
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data

    # Empty Username
    data = {
        "command": "delete_message", 
        "username": "",
        "message_id": "69ee4fc7-8432-40da-99d4-1713e208b568"
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "delete_message", 
        "username": "test",
        "message_id": "69ee4fc7-8432-40da-99d4-1713e208b568"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Username
    data = {
        "command": "delete_message", 
        "username": "",
        "message_id": "69ee4fc7-8432-40da-99d4-1713e208b568"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

def test_server_response():

    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "server_response", 
        "success": True,
        "message": "Message successfully sent"
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Message
    data = {
        "command": "server_response", 
        "success": True,
        "message": ""
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Error Response
    data = {
        "command": "server_response", 
        "success": False,
        "message": "An error occurred"
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "server_response", 
        "success": True,
        "message": "Message successfully sent"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    
    del data["command"] # server responses don't have commmand field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Message
    data = {
        "command": "server_response", 
        "success": True,
        "message": ""
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"] # server responses don't have commmand field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Error Response
    data = {
        "command": "server_response", 
        "success": False,
        "message": "An error occurred"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"] # server responses don't have commmand field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

def test_online_message():
    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "online_message",
        "success": True,
        "message": "Hello",
        "sender": "test",
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Message
    data = {
        "command": "online_message",
        "success": True,
        "message": "",
        "sender": "test"
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Sender
    data = {
        "command": "online_message",
        "success": True,
        "message": "Hello",
        "sender": ""
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "online_message",
        "success": True,
        "message": "Hello",
        "sender": "test"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"] # server responses don't have commmand field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Message
    data = {
        "command": "online_message",
        "success": True,
        "message": "",
        "sender": "test"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"] # server responses don't have commmand field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Sender
    data = {
        "command": "online_message",
        "success": True,
        "message": "Hello",
        "sender": ""
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"] # server responses don't have commmand field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

def test_list_response():
    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "list_response",
        "success": True,
        "matches": ["test1", "test2"],
        "message": "Test"
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # No Matches
    data = {
        "command": "list_response",
        "success": True,
        "matches": [],
        "message": "Test"
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Error Response
    data = {
        "command": "list_response",
        "success": False,
        "matches": [],
        "message": "An error occurred"
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "list_response",
        "success": True,
        "matches": ["test1", "test2"],
        "message": "Test"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # No Matches
    data = {
        "command": "list_response",
        "success": True,
        "matches": [],
        "message": "Test"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Error Response
    data = {
        "command": "list_response",
        "success": False,
        "matches": [],
        "message": "An error occurred"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"
    
def test_read_response():
    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "read_response",
        "success": True,
        "message": "Test",
        "messages": [
            {
                "sender": "test1",
                "message": "Hello",
                "timestamp": 1234567890,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b568"
            },
            {
                "sender": "test2",
                "message": "Hello",
                "timestamp": 1234567890,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b568"
            }
        ]
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # No Messages
    data = {
        "command": "read_response",
        "success": True,
        "message": "Test",
        "messages": []
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Error Response
    data = {
        "command": "read_response",
        "success": False,
        "message": "An error occurred",
        "messages": []
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "read_response",
        "success": True,
        "message": "Test",
        "messages": [
            {
                "sender": "test1",
                "message": "Hello",
                "timestamp": 1234567890,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b568"
            },
            {
                "sender": "test2",
                "message": "Hello",
                "timestamp": 1234567890,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b568"
            }
        ]
    }

    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # No Messages
    data = {
        "command": "read_response",
        "success": True,
        "message": "Test",
        "messages": []
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Error Response
    data = {
        "command": "read_response",
        "success": False,
        "message": "An error occurred",
        "messages": []
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

def test_fetch_sent_messages():
    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "fetch_sent_messages",
        "username": "test",
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Username
    data = {
        "command": "fetch_sent_messages",
        "username": ""
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "fetch_sent_messages",
        "username": "test"
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Empty Username
    data = {
        "command": "fetch_sent_messages",
        "username": ""
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

def test_fetch_sent_messages_response():
    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "fetch_sent_messages_response",
        "success": True,
        "message": "Test",
        "sent_messages": {
            "test1": [{
                "sender": "test1",
                "message": "Hello1",
                "timestamp": 1234567890,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b568"
            },{
                "sender": "test2",
                "message": "Hello2",
                "timestamp": 1234567891,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b567"
            }], 
            "test2": [{
                "sender": "test3",
                "message": "Hello3",
                "timestamp": 1234567892,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b566"
            },{
                "sender": "test4",
                "message": "Hello4",
                "timestamp": 1234567893,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b565"
            }]
        }
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # No Messages
    data = {
        "command": "fetch_sent_messages_response",
        "success": True,
        "message": "Test",
        "sent_messages": {}
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Error Response
    data = {
        "command": "fetch_sent_messages_response",
        "success": False,
        "message": "An error occurred",
        "sent_messages": {}
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "fetch_sent_messages_response",
        "success": True,
        "message": "Test",
        "sent_messages": {
            "test1": [{
                "sender": "test1",
                "message": "Hello1",
                "timestamp": 1234567890,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b568"
            },{
                "sender": "test2",
                "message": "Hello2",
                "timestamp": 1234567891,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b567"
            }], 
            "test2": [{
                "sender": "test3",
                "message": "Hello3",
                "timestamp": 1234567892,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b566"
            },{
                "sender": "test4",
                "message": "Hello4",
                "timestamp": 1234567893,
                "message_id": "69ee4fc7-8432-40da-99d4-1713e208b565"
            }]
        }
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # No Messages
    data = {
        "command": "fetch_sent_messages_response",
        "success": True,
        "message": "Test",
        "sent_messages": {}
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Error Response
    data = {
        "command": "fetch_sent_messages_response",
        "success": False,
        "message": "An error occurred",
        "sent_messages": {}
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

def test_login_response():
    # _____________JSON MODE_____________
    # Typical Case
    data = {
        "command": "login_response",
        "success": True,
        "message": "Test",
        "unread_message_count": 10
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # No Unread Messages
    data = {
        "command": "login_response",
        "success": True,
        "message": "Test",
        "unread_message_count": 0
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Error Response
    data = {
        "command": "login_response",
        "success": False,
        "message": "An error occurred",
        "unread_message_count": 0
    }
    serialized_data = serialize(data, True)
    deserialized_data = deserialize(serialized_data[4:])    # First 4 bytes are length of data
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # _____________WIRE PROTOCOL MODE_____________
    # Typical Case
    data = {
        "command": "login_response",
        "success": True,
        "message": "Test",
        "unread_message_count": 10
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # No Unread Messages
    data = {
        "command": "login_response",
        "success": True,
        "message": "Test",
        "unread_message_count": 0
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"

    # Error Response
    data = {
        "command": "login_response",
        "success": False,
        "message": "An error occurred",
        "unread_message_count": 0
    }
    serialized_data = serialize(data, False)
    deserialized_data = deserialize(serialized_data[9:])    # First 9 bytes are version number and length of data
    del data["command"]  # server responses don't have command field
    assert deserialized_data == data, f"Deserialization failed for data: {data}"