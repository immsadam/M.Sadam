# ============================================
# Workflow Manager & Updater
# Manage ComfyUI workflow JSON files
# ============================================

import json
import os
from pathlib import Path
from typing import Dict, Any, List

class WorkflowManager:
    def __init__(self, workflows_dir="workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.workflows_dir.mkdir(exist_ok=True)
    
    def load_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """
        Load workflow dari file JSON
        
        Args:
            workflow_name (str): Nama workflow (e.g., 'workflow_basic.json')
            
        Returns:
            dict: Workflow JSON
        """
        workflow_path = self.workflows_dir / workflow_name
        
        if not workflow_path.exists():
            print(f"[ERROR] Workflow tidak ditemukan: {workflow_path}")
            return None
        
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
            print(f"[WORKFLOW] Loaded: {workflow_name}")
            return workflow
        
        except Exception as e:
            print(f"[ERROR] Gagal load workflow: {e}")
            return None
    
    def save_workflow(self, workflow: Dict, workflow_name: str):
        """
        Save workflow ke file JSON
        
        Args:
            workflow (dict): Workflow JSON
            workflow_name (str): Nama file output
        """
        workflow_path = self.workflows_dir / workflow_name
        
        try:
            with open(workflow_path, 'w', encoding='utf-8') as f:
                json.dump(workflow, f, indent=2, ensure_ascii=False)
            print(f"[WORKFLOW] Saved: {workflow_path}")
        
        except Exception as e:
            print(f"[ERROR] Gagal save workflow: {e}")
    
    def list_workflows(self) -> List[str]:
        """
        List semua workflow yang tersedia
        
        Returns:
            list: List nama workflow
        """
        workflows = list(self.workflows_dir.glob("*.json"))
        return [w.name for w in workflows]
    
    def get_workflow_info(self, workflow_name: str) -> Dict:
        """
        Ambil informasi workflow
        
        Args:
            workflow_name (str): Nama workflow
            
        Returns:
            dict: Metadata workflow
        """
        workflow = self.load_workflow(workflow_name)
        
        if workflow and '_meta' in workflow and 'workflow_info' in workflow['_meta']:
            return workflow['_meta']['workflow_info']
        
        return {"error": "Workflow info not found"}
    
    def update_prompt(self, workflow: Dict, positive_prompt: str, negative_prompt: str = None) -> Dict:
        """
        Update prompt di workflow
        
        Args:
            workflow (dict): Workflow JSON
            positive_prompt (str): Positive prompt text
            negative_prompt (str, optional): Negative prompt text
            
        Returns:
            dict: Updated workflow
        """
        updated_workflow = workflow.copy()
        
        # Find CLIPTextEncode nodes
        for node_id, node_data in updated_workflow.items():
            if node_data.get('class_type') == 'CLIPTextEncode':
                title = node_data.get('_meta', {}).get('title', '')
                
                if 'Positive' in title:
                    updated_workflow[node_id]['inputs']['text'] = positive_prompt
                    print(f"[WORKFLOW] Updated positive prompt in node {node_id}")
                
                elif 'Negative' in title and negative_prompt:
                    updated_workflow[node_id]['inputs']['text'] = negative_prompt
                    print(f"[WORKFLOW] Updated negative prompt in node {node_id}")
        
        return updated_workflow
    
    def update_seed(self, workflow: Dict, seed: int) -> Dict:
        """
        Update seed di workflow (untuk variasi)
        
        Args:
            workflow (dict): Workflow JSON
            seed (int): Seed value
            
        Returns:
            dict: Updated workflow
        """
        updated_workflow = workflow.copy()
        
        # Find KSampler nodes
        for node_id, node_data in updated_workflow.items():
            if node_data.get('class_type') == 'KSampler':
                updated_workflow[node_id]['inputs']['seed'] = seed
        
        print(f"[WORKFLOW] Updated seed to {seed}")
        return updated_workflow
    
    def update_output_prefix(self, workflow: Dict, prefix: str) -> Dict:
        """
        Update output filename prefix
        
        Args:
            workflow (dict): Workflow JSON
            prefix (str): Output filename prefix
            
        Returns:
            dict: Updated workflow
        """
        updated_workflow = workflow.copy()
        
        # Find SaveImage nodes
        for node_id, node_data in updated_workflow.items():
            if node_data.get('class_type') == 'SaveImage':
                updated_workflow[node_id]['inputs']['filename_prefix'] = prefix
        
        print(f"[WORKFLOW] Updated output prefix to '{prefix}'")
        return updated_workflow
    
    def update_resolution(self, workflow: Dict, width: int, height: int) -> Dict:
        """
        Update resolusi image/video
        
        Args:
            workflow (dict): Workflow JSON
            width (int): Width (e.g., 512, 768, 1024)
            height (int): Height (e.g., 512, 768, 1024)
            
        Returns:
            dict: Updated workflow
        """
        updated_workflow = workflow.copy()
        
        # Find EmptyLatentImage nodes
        for node_id, node_data in updated_workflow.items():
            if node_data.get('class_type') == 'EmptyLatentImage':
                updated_workflow[node_id]['inputs']['width'] = width
                updated_workflow[node_id]['inputs']['height'] = height
        
        print(f"[WORKFLOW] Updated resolution to {width}x{height}")
        return updated_workflow
    
    def update_steps(self, workflow: Dict, steps: int) -> Dict:
        """
        Update jumlah sampling steps
        
        Args:
            workflow (dict): Workflow JSON
            steps (int): Number of steps (e.g., 20, 30, 50)
            
        Returns:
            dict: Updated workflow
        """
        updated_workflow = workflow.copy()
        
        # Find KSampler nodes
        for node_id, node_data in updated_workflow.items():
            if node_data.get('class_type') == 'KSampler':
                updated_workflow[node_id]['inputs']['steps'] = steps
        
        print(f"[WORKFLOW] Updated steps to {steps}")
        return updated_workflow
    
    def update_cfg_scale(self, workflow: Dict, cfg: float) -> Dict:
        """
        Update CFG scale (guidance strength)
        
        Args:
            workflow (dict): Workflow JSON
            cfg (float): CFG scale (e.g., 7.0, 7.5, 8.0)
            
        Returns:
            dict: Updated workflow
        """
        updated_workflow = workflow.copy()
        
        # Find KSampler nodes
        for node_id, node_data in updated_workflow.items():
            if node_data.get('class_type') == 'KSampler':
                updated_workflow[node_id]['inputs']['cfg'] = cfg
        
        print(f"[WORKFLOW] Updated CFG scale to {cfg}")
        return updated_workflow
    
    def update_fps(self, workflow: Dict, fps: int) -> Dict:
        """
        Update FPS untuk video output
        
        Args:
            workflow (dict): Workflow JSON
            fps (int): Frames per second (e.g., 24, 30, 60)
            
        Returns:
            dict: Updated workflow
        """
        updated_workflow = workflow.copy()
        
        # Find VHS_VideoCombine nodes
        for node_id, node_data in updated_workflow.items():
            if node_data.get('class_type') == 'VHS_VideoCombine':
                updated_workflow[node_id]['inputs']['fps'] = fps
        
        print(f"[WORKFLOW] Updated FPS to {fps}")
        return updated_workflow
    
    def update_model(self, workflow: Dict, model_name: str) -> Dict:
        """
        Update checkpoint model
        
        Args:
            workflow (dict): Workflow JSON
            model_name (str): Model filename (e.g., 'sd15_model.safetensors')
            
        Returns:
            dict: Updated workflow
        """
        updated_workflow = workflow.copy()
        
        # Find CheckpointLoaderSimple nodes
        for node_id, node_data in updated_workflow.items():
            if node_data.get('class_type') == 'CheckpointLoaderSimple':
                updated_workflow[node_id]['inputs']['ckpt_name'] = model_name
        
        print(f"[WORKFLOW] Updated model to '{model_name}'")
        return updated_workflow
    
    def validate_workflow(self, workflow: Dict) -> bool:
        """
        Validate workflow structure
        
        Args:
            workflow (dict): Workflow JSON
            
        Returns:
            bool: True jika valid
        """
        try:
            # Check basic structure
            if not isinstance(workflow, dict):
                print("[ERROR] Workflow harus berupa dictionary")
                return False
            
            # Check nodes
            nodes = {k: v for k, v in workflow.items() if k != '_meta'}
            if not nodes:
                print("[ERROR] Workflow tidak memiliki nodes")
                return False
            
            # Check each node
            for node_id, node_data in nodes.items():
                if 'class_type' not in node_data:
                    print(f"[ERROR] Node {node_id} tidak memiliki class_type")
                    return False
                
                if 'inputs' not in node_data:
                    print(f"[ERROR] Node {node_id} tidak memiliki inputs")
                    return False
            
            print(f"[WORKFLOW] ✅ Workflow valid ({len(nodes)} nodes)")
            return True
        
        except Exception as e:
            print(f"[ERROR] Validation error: {e}")
            return False
    
    def export_workflow_for_comfyui(self, workflow: Dict, output_file: str):
        """
        Export workflow untuk digunakan di ComfyUI
        Format ini compatible dengan ComfyUI API
        
        Args:
            workflow (dict): Workflow JSON
            output_file (str): Output file path
        """
        # Remove _meta info sebelum export
        export_workflow = {k: v for k, v in workflow.items() if k != '_meta'}
        
        # Clean up metadata dari setiap node
        for node_id, node_data in export_workflow.items():
            if '_meta' in node_data:
                del export_workflow[node_id]['_meta']
        
        # Save
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_workflow, f, indent=2, ensure_ascii=False)
        
        print(f"[WORKFLOW] Exported for ComfyUI: {output_file}")

if __name__ == "__main__":
    # Test WorkflowManager
    manager = WorkflowManager()
    
    print("\n[TEST] Workflow Manager")
    print("="*50)
    
    # List workflows
    workflows = manager.list_workflows()
    print(f"\nAvailable workflows: {workflows}\n")
    
    # Load workflow
    workflow = manager.load_workflow('workflow_basic.json')
    
    if workflow:
        # Get info
        info = manager.get_workflow_info('workflow_basic.json')
        print(f"\nWorkflow Info:")
        print(json.dumps(info, indent=2, ensure_ascii=False))
        
        # Validate
        print("\nValidating...")
        manager.validate_workflow(workflow)
        
        # Update example
        print("\nUpdating workflow example...")
        updated = manager.update_prompt(
            workflow,
            "A character named Markus walking in the city at night",
            "blurry, distorted, low quality"
        )
        updated = manager.update_resolution(updated, 768, 768)
        updated = manager.update_steps(updated, 30)
        
        # Export
        manager.export_workflow_for_comfyui(updated, 'workflows/workflow_basic_updated.json')
        
        print("\n[TEST] Complete!")
