
// Kết nối socket thông qua LAN (BUILD TRÊN LOCAL)
let socket = io.connect('http://' + document.domain + ':' + location.port);

// Tạo mã phòng để bắt đầu chơi
document.getElementById('create-room-form').addEventListener('submit', function(e) {
    e.preventDefault();
    let roomCode = document.getElementById('create-room-code').value;
    fetch('/create', {
        method: 'POST',
        body: new URLSearchParams({
            'room_code': roomCode,
        })
    }).then(response => {
        if (!response.ok) {
            alert('Tạo phòng không thành công! (Phòng đã tồn tại)');
        } else {
            alert('Tạo phòng thành công --> Hãy tham gia phòng này!');
        }
    });
});

// Lấy room-form từ Frontend để kiểm tra mã phòng 
document.getElementById('join-room-form').addEventListener('submit', function(e) {
    e.preventDefault();
    let roomCode = document.getElementById('join-room-code').value;
    socket.emit('join', { room_code: roomCode }, function(error) {
        if (error) {
            alert("Phòng không tồn tại hoặc đã đủ số người chơi!");
        } else {
            // Ẩn cả khối chứa form tạo phòng và form tham gia phòng
            document.getElementById('create-room-form').parentElement.style.display = 'none';
            document.getElementById('join-room-form').parentElement.style.display = 'none';
            // Hiển thị thông tin về phòng hiện tại và nút để rời phòng
            let currentRoomElement = document.getElementById('current-room');
            currentRoomElement.innerText = 'Phòng hiện tại: ' + roomCode;
            currentRoomElement.style.fontWeight = 'bold';
            document.getElementById('current-room-container').style.display = 'block';
        }
    });
});

// Khi một người chơi rời phòng
document.getElementById('leave-room-button').addEventListener('click', function(e) {
    e.preventDefault();
    // Gửi yêu cầu rời phòng đến server
    socket.emit('leave', { room_code: roomCode }, function(error) {
        location.reload();
    });
});

// Khai báo bảng và người chơi đầu được sử dụng "X"
let boardElement = document.getElementById('board');
let statusElement = document.getElementById('status');
let board = [];
let currentPlayer;

// Tạo biến để theo dõi số lượng người chơi trong phòng
let playerCount = 0;

// Tạo bảng 20x20 
for (let i = 0; i < 20; i++) {
    for (let j = 0; j < 20; j++) {
        let cell = document.createElement('div');
        cell.classList.add('cell');
        cell.addEventListener('click', handleClick, { once: true });
        boardElement.appendChild(cell);
        board.push(cell);
    }
}

