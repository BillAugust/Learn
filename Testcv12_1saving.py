#Code from Testcv112_1_______________________________

            while(nFrames > 0):
               picList.append(blank_image)
               nFrames = nFrames -1
            for j in range(len(runStats)):
                r = runStats[j]
                ostr = str(r.timeStamp)+ " "
                ostr = ostr + str(r.offset) + " "
                ostr = ostr + str(r.correct) + " "
                ostr = ostr + str(r.speedLeft) + " "
                ostr = ostr + str(r.speedRight)
#                 print (ostr)
                
                
#                     " t: ", r.timeStamp,
#                      " off: ", r.offset,
#                      " cor: ", r.correct,
#                      " left: ", r.speedLeft,
#                      " right: ", r.speedRight)
                fdir = "/home/pi/Develop/Learn/images"
                fname = "pic" + str(j) + ".png"
                xco = int(r.offset + camResW/2)
                cv2.line(picList[i],
                         (xco, 0),
                         (xco ,camResH - 1),
                         (255,0,0), 2)
                rotImg = picList[i]
                cv2.putText(rotImg,
                            ostr,
                            (10,30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,(255,255,255),1,1)
#                cv2.imshow(fname,picList[j])
                curDir = os.getcwd()
                os.chdir(fdir)
                cv2.imwrite(fname, rotImg)
                os.chdir(curDir)
#                kn = cv2.waitKey(0)c
                if (kn == ord('q')):
                    break
                cv2.destroyAllWindows()
            car.quit()
            sys.exit()
    except KeyboardInterrupt:
        print("Emergency stop")
        camera.close()
        car.quit()
            
