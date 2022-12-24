import torch.onnx
import onnx

# export model to onnx file 
def Convert_ONNX(model_player, input_size = 50): 
    # set the model to inference mode
    model_player.policy_network.train(False)
    model_player.value_network.train(False)

    # create a dummy input tensor
    dummy_input = torch.randn(1, input_size, requires_grad=True, device="cuda")  

    # export the model   
    torch.onnx.export(model_player.policy_network,  # model being run 
          dummy_input,             # model input (or a tuple for multiple inputs) 
          "Sorting_battle_policy.onnx",     # where to save the model  
          )
    torch.onnx.export(model_player.value_network,   # model being run 
          dummy_input,              # model input (or a tuple for multiple inputs) 
          "Sorting_battle_value.onnx",      # where to save the model  
          )
    print(" ") 
    print('Policy and value model has been converted to ONNX.')

# model_save_P1_name = 'training_model_2P_1_v0.pt'
# path_P1 = f"/content/drive/Shareddrives/ML Final Project/Sorting-Battle-Python/training/model/{model_save_P1_name}"
# model_player1 = torch.load(path_P1)
# Convert_ONNX(model_player1)

# model_save_P2_name = 'training_model_2P_2_v0.pt'
# path_P2 = f"/content/drive/Shareddrives/ML Final Project/Sorting-Battle-Python/training/model/{model_save_P2_name}"
# model_player2 = torch.load(path_P2)
# Convert_ONNX(model_player2)