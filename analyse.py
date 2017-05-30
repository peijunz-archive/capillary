from capillary import edge, fitting, display
import matplotlib.pyplot as plt
for i in range(73):
    plt.clf()
    print('Processing frame %d'%i)
    pts=edge.get(i+1)
    display.show_frame(pts)
    #grid();
    plt.axis('square');
    plt.xlim(0, 284)
    plt.ylim(0, 284)
    plt.savefig('processed/output_%04d_processed.svg'%(i+1),
            bbox_inches='tight',
           ); 
