local internet = component.proxy(component.list("internet")())
local drone = component.proxy(component.list("drone")())

print = function(text)
	return text
end

local x, y, z = 0, 0, 0

drone.getOffset = function()
	return {x=x, y=y, z=z}
end


function resetSocket()
	handle = internet.connect("localhost", 8191)
	print("handle created")
	repeat
		success, err = handle.finishConnect()
		if err then
			handle = internet.connect("localhost", 8191)
		end
	until success
	print("got it")
	return handle
end



function recv(socket, length)
	if length == 0 then
		return true, "", false
	end
	local noerr, data = false
	local t = computer.uptime()
	local timeout = false
	repeat
		noerr, data = pcall(socket.read, length)
	until computer.uptime() - t >= 2 or not noerr or (data and data ~= "")
	if computer.uptime() - t >= 2 then
		timeout = true
	end
	return noerr, data, timeout
end



local sock = resetSocket()

while true do
	local noerr, data, timeout = recv(sock, 2)
	if not timeout and data then	-- if data recv
		local command = data:byte(1)	--get command byte (first)
		local dataLength = data:byte(2)
		print("command : "..tostring(command).."|"..tostring(dataLength))
		local a, ddata, timeout = recv(sock, dataLength)
		
		
		if timeout or command == 0x00 then --command 0x00 (close) or socket crash
			print("close command ("..tostring(timeout)..")")
			sock.close()
			sock = resetSocket()
			
			
		elseif command == 0x01 then	--command 0x01(set status)
			print("status command")
			drone.setStatusText(tostring(ddata))
			
			
		elseif command == 0x02 then	--command 0x02 (move)
			print("move command")
			local ints = ddata:split("|")	--split coords formated like this "x|y|z"
			local offset = drone.getOffset()
			for i in ints do	--string to int
				ints[i] = tonumber(ints[i])
			end
			drone.move(ints[1] - offset.x, ints[2] - offset.y, ints[3] - offset.z) --actual move
			repeat	--wait till at position
				offset = drone.getOffset()
			until ints[1] == offset.x and ints[2] == offset.y and ints[3] == offset.z
			sock.write("ok")	--send signal to serv
			
			
		elseif command == 0x03 then	--command 0x03 (get offset)
			print("offset command")
			local offset = drone.getOffset()
			sock.write(tostring(offset.x).."|"..tostring(offset.y).."|"..tostring(offset.z)) --formating it like this "x|y|z"
		
		
		elseif command == 0x04 then	--command 0x04 (set light color)
			print("light command")
			local light = string.byte(ddata, 1) + 256 * string.byte(ddata, 2) + 65536 * string.byte(ddata, 3) --split rgb (one byte per color)
			drone.setLightColor(light)
		
		
		elseif command == 0x05 then	--command 0x05 (scan) @TODO chunk scan instead of block scan and with other function that just debug.scanCA
			print("scan command")
			local ints = ddata:split("|")
			for i in ints do
				ints[i] = tonumber(ints[i])
			end
			local blocking, label, content = debug.scanContentsAt(ints[1],ints[2], ints[3])
			sock.write(content)
		
		
		elseif command == 0xFF then	--pong command
			sock.write("pong")
		end
	elseif not noerr or (not timeout and (not data or data == "")) then			--timeout
		print("err : "..tostring(noerr))
		sock.close()
		sock = resetSocket()
	else
		print("ping")
		sock.write("ping")
		local t = computer.uptime()
		repeat
			noerr, data = pcall(sock.read, 64)
			if not noerr or computer.uptime() - t > 2 then
				print("timeout, rez")
				sock = resetSocket()
				break
			end
		until data == "pong"
	end
end
