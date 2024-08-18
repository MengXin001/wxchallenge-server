document.addEventListener('DOMContentLoaded', function () {
    let station = "竹子林"
    let data_date = "2024-08-14"
    const rankapi = 'https://api.moexin.cn/api/getRank?date' + data_date;
    let usergroup = []
    fetch("https://api.moexin.cn/api/getUserInfo").then(data => {
        data.json().then((res) => {
            usergroup = res.data
        })
    })
    fetch(rankapi).then(res => {
        res.json().then((data) => {
            const rankingList = document.getElementById('ranking-list');
            rankingList.innerHTML = '';
            const sortedRankings = data["data"].sort((a, b) => a.T_score - b.T_score);
            sortedRankings.forEach((item, index) => {
                const row = document.createElement('tr');
                const rankIcon = index < 3 ? '✨' : '';
                row.innerHTML = `
<td class="whitespace-nowrap py-4 pl-4 pr-3 text-[16px] font-medium text-gray-900 sm:pl-6">${rankIcon} ${index + 1}</td>

<td class="whitespace-nowrap py-4 pl-4 pr-3 text-[16px] sm:pl-6">
    <div class="flex items-center">
        <div class="h-10 w-10 flex-shrink-0">
            <img class="h-10 w-10 rounded-full"
                src="data:image/png;base64,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"
                alt="" />
        </div>
        <div class="ml-4">
            <div class="text-[16px] font-medium text-gray-900">${item.user_nickname}</div>
            <div id="group-list" class="text-[14px] text-gray-500">${usergroup.find(res => res.user_nickname === item.user_nickname).user_school}</div>
        </div>
    </div>
</td>
<td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
    <span class="inline-flex rounded-md bg-[#16a34a33] px-2 text-[14px] font-[500] leading-6 text-green-800">最高气温:
        ${item.max_temp}°C 最低气温: ${item.min_temp}°C 风: ${item.max_wind_speed}m/s Rain24:
        ${item.precipitation}mm</span>
</td>
<td class="whitespace-nowrap px-3 py-4 text-[16px] text-gray-500 text-right">-</td>
<td class="whitespace-nowrap px-3 py-4 text-[16px] text-gray-500 text-right">-</td>`;
                rankingList.appendChild(row);
            });
        })
    })
        .catch(error => {
            console.error(error);
            const rankingList = document.getElementById('ranking-list');
            rankingList.innerHTML = '<li>无数据</li>';
        });
    document.getElementById('date').textContent = `${station + data_date}`;
    const obsapi = 'https://api.moexin.cn/api/getObsData?date=' + data_date;
    fetch(obsapi).then(res => {
        res.json().then((data) => {
            let data_obs = `实况：最高气温：${data.data.max_temp_obs}°C；最低气温：${data.data.min_temp_obs}°C；风：${data.data.max_wind_speed_obs}m/s；24H降水：${data.data.precipitation_obs}mm`
            document.getElementById('obs').textContent = `${data_obs}`;
        }
        )
    })
});
