document.addEventListener('DOMContentLoaded', async function () {
    let station = "福永 G1151 "
    document.getElementById('date').textContent = station
    const today = new Date()

    const dateSelect = document.getElementById('date-select')
    for (let i = 0; i <= 5; i++) {
        const date = new Date()
        date.setDate(today.getDate() - i)
        const formattedDate = date.toISOString().split('T')[0]
        const option = document.createElement('option')
        option.value = formattedDate
        option.textContent = formattedDate
        dateSelect.appendChild(option)
    }
    const groupSelect = document.getElementById('group-select')

    async function groupG(usergroup) {
        groupSelect.innerHTML = `<option value="All">全体成员</option>`
        usergroup.forEach(group => {
            if (!Array.from(groupSelect.options).some(option => option.value === group.user_school)) {
                const option = document.createElement('option')
                option.value = group.user_school
                option.textContent = group.user_school
                groupSelect.appendChild(option)
            }
        })
    }

    async function getData(date, grouplist = false) {
        const rankapi = `https://api.moexin.cn/api/getRank?date=${date}`
        const obsapi = `https://api.moexin.cn/api/getObsData?date=${date}`
        const userapi = "https://api.moexin.cn/api/getUserInfo"
        const userInfoResponse = await fetch(userapi)
        const userInfoData = await userInfoResponse.json()
        let usergroup = userInfoData.data
        if (!grouplist) {
            groupG(usergroup)
        }

        fetch(rankapi).then(res => {
            res.json().then((data) => {
                const rankingList = document.getElementById('ranking-list')
                const selectedGroup = groupSelect.value
                rankingList.innerHTML = ''
                const sortedRankings = data.data.sort((a, b) => a.T_score - b.T_score)
                sortedRankings.forEach((item, index) => {
                    const ug = usergroup.find(res => res.user_nickname === item.user_nickname).user_school
                    if (selectedGroup === "All" || ug === groupSelect.value) {
                        const row = document.createElement('tr')
                        const rankIcon = index < 3 ? '✨' : ''
                        row.innerHTML = `
<td class="whitespace-nowrap py-4 pl-4 pr-3 text-[16px] font-medium text-gray-900 sm:pl-6">${rankIcon} ${index + 1}</td>
<td class="whitespace-nowrap py-4 pl-4 pr-3 text-[16px] sm:pl-6">
    <div class="flex items-center">
        <div class="h-10 w-10 flex-shrink-0">
            <img class="h-10 w-10 rounded-full" 
            src="" alt="" />
        </div>
        <div class="ml-4">
            <div class="text-[16px] font-medium text-gray-900">${item.user_nickname}</div>
            <div id="group-list" class="text-[14px] text-gray-500">${usergroup.find(res => res.user_nickname === item.user_nickname).user_school}</div>
        </div>
    </div>
</td>
<td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
    <span class="inline-flex rounded-md bg-[#16a34a33] px-2 text-[14px] font-[500] leading-6 text-green-800">最高气温: ${item.max_temp}°C 最低气温: ${item.min_temp}°C 最大阵风: ${item.max_wind_speed}m/s 日降雨量: ${item.precipitation}mm</span>
</td>
<td class="whitespace-nowrap px-3 py-4 text-[16px] text-gray-500 text-right">-</td>
<td class="whitespace-nowrap px-3 py-4 text-[16px] text-gray-500 text-right">-</td>`
                        rankingList.appendChild(row)
                    }
                })
            })
        }).catch(error => {
            console.error(error)
            const rankingList = document.getElementById('ranking-list')
            rankingList.innerHTML = '<li>无数据</li>'
        })

        fetch(obsapi).then(res => {
            res.json().then((data) => {
                let data_obs = `实况：最高气温：${data.data.max_temp_obs}°C；最低气温：${data.data.min_temp_obs}°C；最大阵风：${data.data.max_wind_speed_obs}m/s；24H降水：${data.data.precipitation_obs}mm`
                document.getElementById('obs').textContent = data_obs
            })
        })
    }

    getData(today.toISOString().split('T')[0])
    dateSelect.addEventListener('change', function () {
        getData(this.value, true)
    })
    groupSelect.addEventListener('change', function () {
        console.log(groupSelect.value)
        getData(dateSelect.value, true)
    })
})
