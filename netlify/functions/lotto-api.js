exports.handler = async (event) => {
  const round = event.queryStringParameters.round;

  try {
    const response = await fetch(
      `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`
    );
    const data = await response.json();

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        round: data.drwNo,
        date: `${data.drwNoDate}`,
        numbers: [
          data.drwtNo1,
          data.drwtNo2,
          data.drwtNo3,
          data.drwtNo4,
          data.drwtNo5,
          data.drwtNo6,
        ].sort((a, b) => a - b),
        bonus: data.bnusNo,
        prize: {
          1: { count: data.firstPrzwnerCo, amount: data.firstWinamnt },
          2: { count: data.secondPrzwnerCo, amount: data.secondWinamnt },
          3: { count: data.thirdPrzwnerCo, amount: data.thirdWinamnt },
          4: { count: data.fourthPrzwnerCo, amount: data.fourthWinamnt },
          5: { count: data.fifthPrzwnerCo, amount: data.fifthWinamnt },
        },
      }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Failed to fetch lottery data" }),
    };
  }
};
